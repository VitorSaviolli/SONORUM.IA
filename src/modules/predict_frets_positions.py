"""
Função para prever posições de trastes usando calc_axis e geometria do violão
"""
import math
import numpy as np
from .calc_axis import calc_axis

def predict_frets_positions(frame, detected_data, num_frets=12, draw=True):
    """
    Prevê posições de trastes baseado no eixo do violão e geometria musical.
    
    Args:
        frame: imagem onde desenhar
        detected_data: dados das detecções (nut, frets, neck, etc.)
        num_frets: número de trastes a prever (padrão: 12)
        draw: se deve desenhar as previsões no frame
        
    Returns:
        dict com trastes detectadas + previstas
    """
    
    # 1. Calcular eixo do violão com dados detectados
    axis_info = calc_axis(frame, detected_data.get('nut', []), 
                         detected_data.get('frets', []),
                         neck=detected_data.get('neck'),
                         neck_box=detected_data.get('neck_box'),
                         draw=False)  # não desenhar ainda
    
    if not axis_info.get('valid'):
        return detected_data  # retorna dados originais se não conseguir calcular eixo
    
    # 2. Extrair informações do eixo
    nut_point = axis_info['nut_point']
    angle_deg = axis_info['angle_deg']
    projections = axis_info.get('projections', [])
    
    # Converter ângulo para radianos
    angle_rad = math.radians(angle_deg)
    ux = math.cos(angle_rad)  # componente x do vetor unitário
    uy = math.sin(angle_rad)  # componente y do vetor unitário
    
    # 3. Analisar trastes detectadas para calcular escala
    if len(projections) >= 2:
        # Ordenar projeções por distância da pestana
        sorted_projs = sorted(projections, key=lambda p: p['s'])
        
        # Calcular distâncias entre trastes consecutivas
        fret_spacings = []
        for i in range(len(sorted_projs) - 1):
            spacing = sorted_projs[i+1]['s'] - sorted_projs[i]['s']
            fret_spacings.append(spacing)
        
        # Estimar comprimento da escala usando teoria musical
        # A razão entre trastes consecutivas é aproximadamente 1.059463 (12ª raiz de 2)
        if fret_spacings:
            avg_spacing = np.mean(fret_spacings)
            # Estimar comprimento total da escala
            estimated_scale_length = avg_spacing * 17.817  # fator baseado na série harmônica
        else:
            # Fallback: usar distância da pestana ao traste mais distante
            max_dist = max(p['s'] for p in sorted_projs)
            estimated_scale_length = max_dist * 2.0
    else:
        # Fallback: estimar escala baseado no tamanho da imagem
        h, w = frame.shape[:2]
        estimated_scale_length = min(w, h) * 0.6
    
    # 4. Calcular posições teóricas dos trastes
    predicted_frets = []
    fret_ratio = 17.817  # Constante para divisão da escala (12ª raiz de 2 - 1)
    
    for fret_num in range(1, num_frets + 1):
        # Fórmula musical: distância = scale_length * (1 - (2^(-fret_num/12)))
        theoretical_distance = estimated_scale_length * (1 - math.pow(2, -fret_num/12))
        
        # Posição no eixo
        pred_x = nut_point[0] + ux * theoretical_distance
        pred_y = nut_point[1] + uy * theoretical_distance
        
        # Verificar se está dentro da imagem
        if 0 <= pred_x < frame.shape[1] and 0 <= pred_y < frame.shape[0]:
            predicted_frets.append({
                'fret_number': fret_num,
                'position': (int(pred_x), int(pred_y)),
                'distance_from_nut': theoretical_distance,
                'confidence': 0.85,  # alta confiança para previsões teóricas
                'type': 'predicted'
            })
    
    # 5. Combinar trastes detectadas com previstas
    detected_frets = detected_data.get('frets', [])
    combined_frets = []
    
    # Adicionar trastes detectadas
    for i, (fx, fy, conf) in enumerate(detected_frets):
        combined_frets.append({
            'fret_number': i + 1,  # estimativa
            'position': (fx, fy),
            'confidence': conf,
            'type': 'detected'
        })
    
    # Adicionar trastes previstas (evitando sobreposição)
    for pred_fret in predicted_frets:
        px, py = pred_fret['position']
        
        # Verificar se há traste detectada muito próxima
        too_close = False
        for det_fret in combined_frets:
            if det_fret['type'] == 'detected':
                dx = px - det_fret['position'][0]
                dy = py - det_fret['position'][1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < 30:  # threshold de proximidade
                    too_close = True
                    break
        
        if not too_close:
            combined_frets.append(pred_fret)
    
    # 6. Desenhar previsões se solicitado
    if draw:
        try:
            import cv2
            
            # Desenhar eixo
            start_pt, end_pt = axis_info['axis']
            cv2.line(frame, start_pt, end_pt, (0, 255, 255), 2)
            
            # Desenhar trastes previstas
            for fret in combined_frets:
                px, py = fret['position']
                if fret['type'] == 'predicted':
                    # Círculo azul para previstas
                    cv2.circle(frame, (px, py), 4, (255, 0, 0), -1)
                    # Número do traste
                    cv2.putText(frame, str(fret['fret_number']), 
                              (px + 8, py - 8), cv2.FONT_HERSHEY_SIMPLEX, 
                              0.4, (255, 0, 0), 1)
                else:
                    # Círculo verde para detectadas
                    cv2.circle(frame, (px, py), 4, (0, 255, 0), -1)
                    
        except ImportError:
            pass
    
    # 7. Retornar dados combinados
    result = detected_data.copy()
    result['predicted_frets'] = combined_frets
    result['axis_info'] = axis_info
    result['estimated_scale_length'] = estimated_scale_length
    
    return result


def improve_fret_detection_with_geometry(detected_data, axis_info):
    """
    Melhora detecções usando geometria e padrões musicais.
    
    Args:
        detected_data: dados das detecções originais
        axis_info: informações do eixo calculado
        
    Returns:
        dados com detecções melhoradas
    """
    if not axis_info.get('valid'):
        return detected_data
        
    projections = axis_info.get('projections', [])
    if len(projections) < 2:
        return detected_data
    
    # Ordenar por distância da pestana
    sorted_projs = sorted(projections, key=lambda p: p['s'])
    
    # Identificar outliers baseado em espaçamento esperado
    spacings = []
    for i in range(len(sorted_projs) - 1):
        spacing = sorted_projs[i+1]['s'] - sorted_projs[i]['s']
        spacings.append(spacing)
    
    if spacings:
        median_spacing = sorted(spacings)[len(spacings)//2]
        
        # Filtrar trastes com espaçamento anômalo
        filtered_frets = [sorted_projs[0]]  # sempre manter a primeira
        
        for i in range(1, len(sorted_projs)):
            current_spacing = sorted_projs[i]['s'] - filtered_frets[-1]['s']
            
            # Aceitar se espaçamento está numa faixa razoável
            if 0.3 * median_spacing <= current_spacing <= 2.5 * median_spacing:
                filtered_frets.append(sorted_projs[i])
        
        # Atualizar dados
        improved_frets = [(p['pt'][0], p['pt'][1], p['conf']) for p in filtered_frets]
        
        result = detected_data.copy()
        result['frets'] = improved_frets
        result['original_frets'] = detected_data.get('frets', [])
        
        return result
    
    return detected_data
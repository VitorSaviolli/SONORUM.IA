"""
    frets = [] # trastes
    nut = [] # parte branca
    neck = [] # braço
"""

def calc_axis(frame, nut, frets, neck=None, neck_box=None, draw=True, min_confidence=0.3):
    """
    Calcula o eixo do violão baseado na pestana e trastes.
    
    Args:
        frame: imagem onde desenhar
        nut: lista de detecções da pestana [(x,y,conf), ...]
        frets: lista de detecções dos trastes [(x,y,conf), ...]
        neck: lista de detecções do braço [(x,y,conf), ...] (opcional)
        neck_box: lista de caixas do braço [((x1,y1),(x2,y2),conf), ...] (opcional)
        draw: se deve desenhar no frame
        min_confidence: confiança mínima para filtrar detecções fracas
        
    Returns: dict com dados do eixo
    """
    import math

    out = {'valid': False, 'nut_point': None, 'mean_frets': None, 'axis': None, 'angle_deg': None, 'projections': []}

    # Filtra frets por confiança mínima
    filtered_frets = [f for f in frets if len(f) >= 3 and f[2] >= min_confidence]
    
    if not filtered_frets:
        return out

    # Filtra nut por confiança
    filtered_nut = [n for n in nut if len(n) >= 3 and n[2] >= min_confidence]

    # choose nut
    if filtered_nut:
        nut_pt = (int(filtered_nut[0][0]), int(filtered_nut[0][1]))
    else:
        # fallback to top-most fret
        fx = min(filtered_frets, key=lambda x: x[1])
        nut_pt = (int(fx[0]), int(fx[1]))

    # mean of frets
    sx = sy = 0.0
    for cx, cy, _ in filtered_frets:
        sx += cx; sy += cy
    mean_x = sx / len(filtered_frets)
    mean_y = sy / len(filtered_frets)
    mean_pt = (int(mean_x), int(mean_y))

    dx = mean_x - nut_pt[0]
    dy = mean_y - nut_pt[1]
    norm = math.hypot(dx, dy)
    if norm < 1e-6:
        return out
    ux = dx / norm
    uy = dy / norm

    # axis endpoints for drawing - limitar ao braço se disponível
    h, w = frame.shape[:2]
    
    if neck_box and len(neck_box) > 0:
        # Usar caixa do braço para limitar a linha
        (x1, y1), (x2, y2), _ = neck_box[0]
        neck_left = max(0, x1)
        neck_right = min(w, x2)
        neck_top = max(0, y1)
        neck_bottom = min(h, y2)
        
    elif neck and len(neck) > 0:
        # Usar centro do braço e estimar dimensões
        neck_cx, neck_cy = neck[0][:2]
        
        # Estimar dimensões do braço baseado no tamanho da imagem
        estimated_neck_w = w // 3  # aprox 1/3 da largura
        estimated_neck_h = h // 2  # aprox 1/2 da altura
        
        # Limites do braço
        neck_left = max(0, int(neck_cx - estimated_neck_w//2))
        neck_right = min(w, int(neck_cx + estimated_neck_w//2))
        neck_top = max(0, int(neck_cy - estimated_neck_h//2))
        neck_bottom = min(h, int(neck_cy + estimated_neck_h//2))
    else:
        # Sem detecção do braço: usar imagem inteira com linha mais curta
        neck_left, neck_top = 0, 0
        neck_right, neck_bottom = w, h
    
    # Calcular endpoints da linha
    if (neck_box or neck) and abs(ux) > 1e-6:
        # Calcular intersecções da linha com os limites do braço
        # Intersecção com bordas esquerda/direita
        t_left = (neck_left - nut_pt[0]) / ux
        t_right = (neck_right - nut_pt[0]) / ux
        
        y_left = nut_pt[1] + uy * t_left
        y_right = nut_pt[1] + uy * t_right
        
        # Verificar se intersecções estão dentro dos limites Y do braço
        valid_left = neck_top <= y_left <= neck_bottom
        valid_right = neck_top <= y_right <= neck_bottom
        
        if valid_left and valid_right:
            start = (neck_left, int(y_left))
            end = (neck_right, int(y_right))
        elif valid_left:
            start = (neck_left, int(y_left))
            # Limitar para não sair muito da área do braço
            max_extend = min(200, (neck_right - neck_left) // 2)
            end = (int(nut_pt[0] + ux * max_extend), int(nut_pt[1] + uy * max_extend))
        elif valid_right:
            # Limitar para não sair muito da área do braço
            max_extend = min(200, (neck_right - neck_left) // 2)
            start = (int(nut_pt[0] - ux * max_extend), int(nut_pt[1] - uy * max_extend))
            end = (neck_right, int(y_right))
        else:
            # Fallback: linha curta centrada
            length = min(100, (neck_right - neck_left) // 3)
            start = (int(nut_pt[0] - ux * length), int(nut_pt[1] - uy * length))
            end = (int(nut_pt[0] + ux * length), int(nut_pt[1] + uy * length))
    else:
        # Sem braço detectado ou linha vertical: linha mais conservadora
        length = min(w, h) // 4  # ainda menor
        start = (int(nut_pt[0] - ux * length), int(nut_pt[1] - uy * length))
        end = (int(nut_pt[0] + ux * length), int(nut_pt[1] + uy * length))

    angle_deg = math.degrees(math.atan2(uy, ux))

    out.update({'valid': True, 'nut_point': nut_pt, 'mean_frets': mean_pt, 'axis': (start, end), 'angle_deg': angle_deg})

    # project each fret onto the axis and compute scalar s
    projections = []
    for cx, cy, conf in frets:
        rx = cx - nut_pt[0]
        ry = cy - nut_pt[1]
        s = rx * ux + ry * uy
        proj_x = int(nut_pt[0] + ux * s)
        proj_y = int(nut_pt[1] + uy * s)
        projections.append({'pt': (int(cx), int(cy)), 'proj': (proj_x, proj_y), 's': s, 'conf': conf})

    out['projections'] = projections

    return out
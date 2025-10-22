import cv2 

def draw(data, frame, allowed_classes):
    if allowed_classes is None or "frets" in allowed_classes:
        for (cx, cy, conf) in data['frets']:
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), 2)
    if allowed_classes is None or "frets_box" in allowed_classes:
        for (pt1, pt2, conf) in data['frets_box']:
            x1, y1 = pt1
            x2, y2 = pt2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if allowed_classes is None or "nut" in allowed_classes:
        for (cx, cy, conf) in data['nut']:
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), 2)

    if allowed_classes is None or "neck" in allowed_classes:
        for (pt1, pt2, conf) in data['neck_box']:
            x1, y1 = pt1
            x2, y2 = pt2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    if 'valid' in data and data['valid']:
        if allowed_classes is None or "axis" in allowed_classes:
            start, end = data['axis']
            cv2.line(frame, start, end, (0, 255, 255), 2)
        if allowed_classes is None or "projections" in allowed_classes:
            for p in data['projections']:
                pt = p.get('pt')
                proj = p.get('proj')
                if pt and proj:
                    cv2.circle(frame, pt, 3, (0, 200, 0), -1)
                    cv2.circle(frame, proj, 3, (0, 0, 200), -1)
                    cv2.line(frame, pt, proj, (200, 200, 0), 1)
    
    # Desenhar trastes previstas
    if 'predicted_frets' in data and (allowed_classes is None or "predicted_frets" in allowed_classes):
        for fret in data['predicted_frets']:
            px, py = fret['position']
            fret_num = fret.get('fret_number', '?')
            fret_type = fret.get('type', 'unknown')
            
            if fret_type == 'predicted':
                # Círculo azul para previstas
                cv2.circle(frame, (px, py), 6, (255, 100, 0), -1)  # azul mais forte
                cv2.circle(frame, (px, py), 8, (255, 150, 0), 2)   # borda
                # Número do traste
                cv2.putText(frame, f"F{fret_num}", (px + 10, py - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)
            elif fret_type == 'detected':
                # Círculo verde para detectadas (melhoradas)
                cv2.circle(frame, (px, py), 5, (0, 255, 100), -1)
                cv2.circle(frame, (px, py), 7, (0, 255, 150), 2)
    
    # Desenhar ponto médio das trastes se disponível
    if 'mean_frets' in data and (allowed_classes is None or "mean_frets" in allowed_classes):
        mean_pt = data['mean_frets']
        if mean_pt:
            cv2.circle(frame, mean_pt, 8, (0, 255, 0), -1)
            cv2.circle(frame, mean_pt, 12, (0, 200, 0), 2)

    return frame

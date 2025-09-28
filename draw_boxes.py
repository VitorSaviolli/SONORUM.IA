import cv2 

def draw(data, frame, allowed_classes):
    if (allowed_classes is None or "fret" in allowed_classes) and 'frets' in data:
            for(cx,cy,conf) in data['frets']:
                cv2.circle(frame, (cx,cy), 5, (0,255,0), -1)
                # cv2.putText(frame, f'fret {conf:.2f}', (cx+5,cy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    if (allowed_classes is None or "nut" in allowed_classes) and 'nut' in data:
            for(cx,cy,conf) in data['nut']:
                cv2.circle(frame, (cx,cy), 5, (255,0,0), -1)
                # cv2.putText(frame, f'nut {conf:.2f}', (cx+5,cy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    if (allowed_classes is None or "neck" in allowed_classes) and 'neck' in data:
            for(cx,cy,conf) in data['neck']:
                cv2.circle(frame, (cx,cy), 5, (0,0,255), -1)
                # cv2.putText(frame, f'neck {conf:.2f}', (cx+5,cy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    return frame
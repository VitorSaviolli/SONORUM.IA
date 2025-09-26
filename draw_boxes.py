import cv2 

def draw(results, frame, allowed_classes):
    for r in results:
        # boxes recebes cada bouding box identificada ao longo do for em q r percorre results
        boxes = r.boxes
        for box in boxes:
            # box recebe do bouding box suas coordendas da ponta superior esquerda e inferior direita {(x1,y1) e (x2,y2) respectivamente}
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            
            # conf = % de crtz daquele objeto ser de fato aquela classe
            # label recebe o nome das classes e forma uma lista
            conf = float(box.conf[0])
            classes = int(box.cls[0])
            label = r.names[classes]
            txt = f'{label} {conf:.2f}'
            
            if allowed_classes and label not in allowed_classes:
                continue

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0),2)
            cv2.putText(frame, txt, (x1,y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return frame
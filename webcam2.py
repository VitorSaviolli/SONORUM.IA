import cv2
import numpy as np
from ultralytics import YOLO

# modelo YOLO DETECT
model = YOLO(r"C:\Users\Pedro\Documents\Estudos\IF 4°\PICO\yolo_guitar\runs\detect\train\weights\best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    if results.boxes is None or len(results.boxes) == 0:
        cv2.imshow("Casas e Cordas", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    boxes = results.boxes.xyxy.cpu().numpy().astype(int)
    classes = results.boxes.cls.cpu().numpy().astype(int)

    frets = []
    nut = None
    neck = None

    for cls, box in zip(classes, boxes):
        x1, y1, x2, y2 = box
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if cls == 0:  # fret
            frets.append((cx, cy))
        elif cls == 1:  # neck
            neck = (x1, y1, x2, y2)
        elif cls == 2:  # nut
            nut = (cx, cy)

    frets = sorted(frets, key=lambda x: x[0])

    if neck is not None:
        y_top = neck[1]
        y_bottom = neck[3]
    elif frets:
        y_top = min(y for _, y in frets) - 20
        y_bottom = max(y for _, y in frets) + 20
    else:
        y_top, y_bottom = 0, frame.shape[0]

    if nut is not None and frets:
        casas = {}
        x_positions = [nut[0]] + [f[0] for f in frets]  # nut + trastes
        altura = y_bottom - y_top
        espaco_corda = altura / 6

        for i in range(len(x_positions) - 1):
            x_esq = x_positions[i]
            x_dir = x_positions[i + 1]

            casas[i+1] = {}
            for corda in range(6):  # 6 cordas
                y_corda = int(y_top + (corda + 0.5) * espaco_corda)
                x_corda = int((x_esq + x_dir) / 2)
                casas[i+1][corda+1] = (x_corda, y_corda)

                # desenhar ponto
                cv2.circle(frame, (x_corda, y_corda), 5, (0,0,255), -1)
                cv2.putText(frame, f"{corda+1},{i+1}", (x_corda+5, y_corda-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1)

    cv2.imshow("Casas e Cordas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

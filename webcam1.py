import cv2
from ultralytics import YOLO
import numpy as np

# carrega o modelo YOLO treinado (detecção)
model = YOLO(r"C:\Users\Pedro\Documents\Estudos\IF 4°\PICO\yolo_guitar\runs\detect\train\weights\best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]  # resultados da detecção

    if results.boxes is None or len(results.boxes) == 0:
        cv2.imshow("YOLO - Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    classes = results.boxes.cls.cpu().numpy().astype(int)
    boxes = results.boxes.xyxy.cpu().numpy().astype(int)

    frets = []
    nut = None
    neck = None

    for cls, box in zip(classes, boxes):
        x1, y1, x2, y2 = box
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # desenhar bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        if cls == 0:  # fret
            frets.append((cx, cy))
        elif cls == 1:  # neck
            neck = (x1, y1, x2, y2)
        elif cls == 2:  # nut
            nut = (cx, cy)

    if len(frets) >= 3:
        frets = sorted(frets, key=lambda x: x[0])  # ordenar

        # 3ª casa (entre fret2 e fret3)
        casa3_x = int((frets[2][0] + frets[1][0]) / 2)
        casa3_y = int((frets[2][1] + frets[1][1]) / 2)

        cv2.circle(frame, (casa3_x, casa3_y), 8, (0, 0, 255), -1)

    cv2.imshow("YOLO - Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
from ultralytics import YOLO
import numpy as np

# carrega o modelo treinado com YOLO11n (detecção, não segmentação)
model = YOLO(r"C:\Users\Pedro\Documents\Estudos\IF 4°\PICO\yolo_guitar\runs\detect\train\weights\best.pt")

frame = cv2.imread("violao.jpg")

results = model(frame)

print("Resultados:", results)

for r in results:
    if r.boxes is None:
        print("Nenhuma detecção encontrada.")
        continue

    classes = r.boxes.cls.cpu().numpy().astype(int)
    boxes = r.boxes.xyxy.cpu().numpy().astype(int)  # [x1, y1, x2, y2]

    frets = []
    nut = None
    neck = None

    for cls, box in zip(classes, boxes):
        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # desenhar bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        if cls == 0:  # fret
            frets.append((cx, cy))
        elif cls == 1:  # neck
            neck = (x1, y1, x2, y2)
        elif cls == 2:  # nut
            nut = (cx, cy)

    # se detectou pelo menos 3 trastes
    if len(frets) >= 3:
        frets = sorted(frets, key=lambda x: x[0])  # ordenar da esquerda p/ direita

        # exemplo: pegar a 3ª casa (meio entre fret2 e fret3)
        casa3_x = int((frets[2][0] + frets[1][0]) / 2)
        casa3_y = int((frets[2][1] + frets[1][1]) / 2)

        cv2.circle(frame, (casa3_x, casa3_y), 8, (0, 0, 255), -1)

# mostrar resultado
cv2.namedWindow("saida", cv2.WINDOW_NORMAL)
cv2.imshow("saida", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

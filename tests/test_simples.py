import cv2
from ultralytics import YOLO
import numpy as np

model = YOLO(r"C:\Users\Pedro\Documents\Estudos\IF 4°\PICO\yolo_guitar\runs\segment\train\weights\best.pt")

frame = cv2.imread("violao.jpg")

results = model(frame)

print("Resultados:", results)

for r in results:
    if r.boxes is None or r.masks is None:
        print("Nenhuma detecção encontrada.")
        continue

    classes = r.boxes.cls.cpu().numpy().astype(int)
    masks = r.masks.xy  # lista de polígonos

    frets = []
    nut = None
    neck = None

    for cls, mask in zip(classes, masks):
        pts = np.array(mask, dtype=np.int32)

        # desenhar contorno da máscara
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

        # calcular centroide
        M = cv2.moments(pts)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        if cls == 0:  # fret
            frets.append((cx, cy))
        elif cls == 1:  # neck
            neck = pts
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
cv2.resizeWindow("saida", frame.shape[1], frame.shape[0])
cv2.imshow("saida", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

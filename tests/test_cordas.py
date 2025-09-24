import cv2
import numpy as np
from ultralytics import YOLO

# modelo correto: treinado em modo DETECT
model = YOLO("runs/detect/train/weights/best.pt")

frame = cv2.imread("violao.jpg")
print(f"Dimensões da imagem original: {frame.shape}")
results = model(frame)[0]  # só 1 imagem

# --- pegar predições ---
boxes = results.boxes.xyxy.cpu().numpy().astype(int)  # [x1,y1,x2,y2]
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
        neck = (x1, y1, x2, y2)  # caixa do braço
    elif cls == 2:  # nut
        nut = (cx, cy)

# --- ordenar trastes da esquerda pra direita ---
frets = sorted(frets, key=lambda x: x[0])

# --- pegar limites verticais do braço (neck) ---
if neck is not None:
    y_top = neck[1]
    y_bottom = neck[3]
else:
    y_top = min(y for _, y in frets) - 20
    y_bottom = max(y for _, y in frets) + 20

# --- criar casas ---
casas = {}
x_positions = [nut[0]] + [f[0] for f in frets]  # nut + todos trastes

for i in range(len(x_positions)-1):
    x_esq = x_positions[i]
    x_dir = x_positions[i+1]

    casas[i+1] = {}
    altura = y_bottom - y_top
    espaco_corda = altura / 6

    for corda in range(6):  # 0 a 5 -> cordas 1 a 6
        y_corda = int(y_top + (corda + 0.5) * espaco_corda)
        x_corda = int((x_esq + x_dir) / 2)
        casas[i+1][corda+1] = (x_corda, y_corda)

        # desenhar ponto na imagem
        cv2.circle(frame, (x_corda, y_corda), 5, (0,0,255), -1)
        cv2.putText(frame, f"{corda+1},{i+1}", (x_corda+5,y_corda-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1)

cv2.namedWindow("Casas e Cordas", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Casas e Cordas", frame.shape[1], frame.shape[0])
cv2.imshow("Casas e Cordas", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
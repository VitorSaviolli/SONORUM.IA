import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("runs/segment/train/weights/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    # --- pegar predições ---
    # Adicione uma verificação para evitar erros se nenhuma máscara ou caixa for detectada
    if results.masks is not None and results.boxes is not None:
        masks = results.masks.xy
        classes = results.boxes.cls.cpu().numpy().astype(int)

        frets = []
        nut = None
        neck = None

        for cls, mask in zip(classes, masks):
            pts = np.array(mask, dtype=np.int32)
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

        # --- Verificação para evitar erros se o braço ou a pestana não forem detectados ---
        if neck is not None and nut is not None:
            # --- ordenar trastes da esquerda pra direita ---
            frets = sorted(frets, key=lambda x: x[0])

            # --- pegar limites verticais do braço (neck) ---
            y_top = np.min(neck[:, 1])
            y_bottom = np.max(neck[:, 1])

            # --- criar casas ---
            casas = {}
            x_positions = [nut[0]] + [f[0] for f in frets]  # nut + todos trastes

            for i in range(len(x_positions) - 1):
                x_esq = x_positions[i]
                x_dir = x_positions[i + 1]

                altura = y_bottom - y_top
                if altura > 0:
                    espaco_corda = altura / 6
                    for corda in range(6):  # 0 a 5 -> cordas 1 a 6
                        y_corda = int(y_top + (corda + 0.5) * espaco_corda)
                        x_corda = int((x_esq + x_dir) / 2)

                        # desenhar ponto na imagem
                        cv2.circle(frame, (x_corda, y_corda), 5, (0, 0, 255), -1)
                        cv2.putText(frame, f"{corda + 1},{i + 1}", (x_corda + 5, y_corda - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

    # mostrar resultado
    cv2.imshow("YOLO - Webcam", frame)

    # sair com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 
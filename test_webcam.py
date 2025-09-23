import cv2
from ultralytics import YOLO
import numpy as np

model = YOLO(r"C:\Users\Pedro\Documents\Estudos\IF 4°\PICO\yolo_guitar\runs\segment\train\weights\best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # rodar modelo na webcam
    results = model(frame)

    for r in results:
        if r.masks is None:
            continue

        classes = r.boxes.cls.cpu().numpy().astype(int)
        masks = r.masks.xy

        for cls, mask in zip(classes, masks):
            pts = np.array(mask, dtype=np.int32)
            color = (255, 0, 0) if cls == 0 else (0, 255, 0) if cls == 1 else (0, 0, 255)
            cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)

    # mostrar resultado
    cv2.imshow("YOLO - Webcam", frame)

    # sair com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

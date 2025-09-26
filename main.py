from ultralytics import YOLO
from draw_boxes import draw
import cv2

model = YOLO("runs/detect/train/weights/best.pt")
cap = cv2.VideoCapture(0)
allowed_classes = None

while True:
    ret, frame = cap.read()
    if not ret: 
        print("Erro, nenhum vídeo identificado")
        break

    results = model(frame)
    frame_draw = draw(results, frame, allowed_classes)  

    cv2.imshow("Sonorum", frame_draw)
    key = cv2.waitKey(1) &  0xFF
    if key == ord('q'):
        print("Aplicativo finalizado")
        break
    elif key == ord('1'):
        allowed_classes = ['fret','nut']
    elif key == ord('2'):
        allowed_classes = ['fret']
    elif key == ord('3'):
        allowed_classes = ['nut']
    elif key == ord('4'):
        allowed_classes = None

cap.release
cv2.destroyAllWindows()

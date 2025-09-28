from ultralytics import YOLO
from draw_boxes import draw
from collect_data import collect
import cv2

model = YOLO("runs/detect/train/weights/best.pt")
cap = cv2.VideoCapture(0)
allowed_classes = None

while True:
    ret, frame = cap.read()
    if not ret: 
        print("Erro, nenhum vídeo identificado")
        break

    # frame = cv2.imread("violao.jpg")

    results = model(frame)
    data = collect(results)
    print("Trastes (x,y,conf): ", data['frets'])
    print("Pestana (x,y,conf): ", data['nut'])
    print("Braço (x,y,conf): ", data['neck'])

    frame_draw = draw(data, frame, allowed_classes)  

    cv2.imshow("Sonorum", frame_draw)
    key = cv2.waitKey(1) &  0xFF
    if key == ord('q'):
        print("Aplicativo finalizado")
        break
    elif key == ord('1'):
        allowed_classes = ['frets','frets_box','nut']
    elif key == ord('2'):
        allowed_classes = ['frets','frets_box']
    elif key == ord('3'):
        allowed_classes = ['frets','nut']
    elif key == ord('4'):
        allowed_classes = None

cap.release
cv2.destroyAllWindows()

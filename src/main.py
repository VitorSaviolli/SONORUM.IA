from ultralytics import YOLO
from modules.draw_boxes import draw
from modules.calc_axis import calc_axis
from modules.collect_data import collect
from modules.predict_frets_positions import predict_frets_positions, improve_fret_detection_with_geometry
import cv2

model = YOLO("../runs/detect/train/weights/best.onnx")
cap = cv2.VideoCapture(0)
allowed_classes = None

while True:
    # ret, frame = cap.read()
    # if not ret: 
    #     print("Erro, nenhum vídeo identificado")
    #     break

    frame = cv2.imread("../violao.jpg")

    results = model(frame)
    data = collect(results)
    
    # Melhorar detecções usando geometria
    axis = calc_axis(frame, data['nut'], data['frets'], 
                     neck=data.get('neck'), neck_box=data.get('neck_box'),
                     draw=False, min_confidence=0.4)
    
    # Aplicar filtro geométrico para melhorar detecções
    improved_data = improve_fret_detection_with_geometry(data, axis)
    
    # Prever posições de trastes baseado no eixo e geometria musical
    predicted_data = predict_frets_positions(frame, improved_data, num_frets=12, draw=True)
    
    # Usar dados melhorados
    data.update(predicted_data)



    frame_draw = draw(data, frame, allowed_classes)  

    cv2.imshow("Sonorum", frame_draw)
    key = cv2.waitKey(1) & 0xFF
    

    match key:
        case k if k == ord('q'):
            print("Aplicativo finalizado")
            break
        case k if k == ord('1'):
            # TUDO
            allowed_classes = ['frets', 'frets_box', 'nut', 'axis']
        case k if k == ord('2'):
            # APENAS TRASTES
            allowed_classes = ['frets', 'frets_box', 'projections', 'mean_frets']
        case k if k == ord('3'):
            # APENAS PROJEÇÃO
            allowed_classes = ['projections']
        case k if k == ord('4'):
            # PROJEÇÃO COMPARADO A CENTROIDES
            allowed_classes = ['projections', 'frets']
        case k if k == ord('5'):
            allowed_classes = None
        case k if k == ord('6'):
            # APENAS PREDIÇÕES
            allowed_classes = ['predicted_frets', 'axis']
        case k if k == ord('7'):
            # DETECTADAS + PREDITAS
            allowed_classes = ['frets', 'predicted_frets', 'axis']
        case k if k == ord('8'):
            # ANÁLISE COMPLETA
            allowed_classes = ['frets', 'predicted_frets', 'axis', 'projections', 'nut']
        case _:
            pass  # ignora outras teclas

cap.release()
cv2.destroyAllWindows()

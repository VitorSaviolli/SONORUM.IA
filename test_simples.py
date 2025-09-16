import cv2
from ultralytics import YOLO

# Carregar modelo
model = YOLO("runs/pose/train/weights/best.pt")

# Carregar imagem
frame = cv2.imread("WIN_20250909_16_12_13_Pro.jpg")

# Fazer predição
results = model(frame)

# Pega nomes das classes (vem do data.yaml)
names = model.names  

for r in results:
    # --- BOUNDING BOXES ---
    boxes = r.boxes.xyxy.cpu().numpy().astype(int)   # [x1, y1, x2, y2]
    cls_ids = r.boxes.cls.cpu().numpy().astype(int)  # IDs das classes
    
    for box, cls in zip(boxes, cls_ids):
        x1, y1, x2, y2 = box
        label = names[int(cls)] if int(cls) in names else str(cls)

        # desenhar retângulo
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # escrever nome da classe
        cv2.putText(frame, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)]
    # --- KEYPOINTS ---
    if r.keypoints is not None:
        kpts = r.keypoints.xy.cpu().numpy()  # (N objetos, K pontos, 2 coords)

        for obj_id, person in enumerate(kpts):
            for kp_id, (x, y) in enumerate(person):
                if x > 0 and y > 0:  # ignora pontos "vazios"
                    # desenha ponto
                    color = colors[kp_id//2]
                    cv2.circle(frame, (int(x), int(y)), 5, color, -1)
                    # escreve id do ponto
                    cv2.putText(frame, str(kp_id), (int(x) + 5, int(y) - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

# Mostrar resultado
cv2.imshow("YOLO Pose + Boxes", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

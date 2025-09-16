import numpy as np
import cv2
from ultralytics import YOLO

# Carregar o modelo treinado
model = YOLO("runs/pose/train/weights/best.pt")

# Carregar a imagem
frame = cv2.imread("WIN_20250909_16_12_13_Pro.jpg")

# Fazer predição
results = model(frame)

# Pegar keypoints do primeiro objeto detectado
if len(results[0].keypoints.xy) > 0:
    keypoints = results[0].keypoints.xy[0].cpu().numpy()
    keypoints = [tuple(map(int, kp)) for kp in keypoints]  # [(x,y), ...]
else:
    keypoints = []

# Função para calcular posições dos trastes
def calcular_trastes(p_inicio, p_fim, n_trastes=12):
    x0, y0 = p_inicio
    x1, y1 = p_fim
    L = np.linalg.norm([x1 - x0, y1 - y0])
    posicoes = [L - (L / (2**(i/12))) for i in range(1, n_trastes+1)]
    t_values = [d / L for d in posicoes]
    trastes = []
    for t in t_values:
        x = (1 - t) * x0 + t * x1
        y = (1 - t) * y0 + t * y1
        trastes.append((int(x), int(y)))
    return trastes

# Criar mapa (corda, traste)
mapa = {}
for i in range(6):  # 6 cordas
    p_inicio = keypoints[2*i]
    p_fim = keypoints[2*i + 1]
    casas = calcular_trastes(p_inicio, p_fim, n_trastes=12)
    mapa[i+1] = casas

print("Coordenada da corda 6 (E grave), casa 1:", mapa[6][0])
print("Coordenada da corda 1 (E agudo), casa 5:", mapa[1][4])

# Desenhar todos os pontos na imagem
for corda, casas in mapa.items():
    for (x, y) in casas:
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

cv2.imshow("Mapa de casas", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sugestões para melhorar a detecção de trastes

## Problemas identificados:
1. **Nem todas as trastes são detectadas** - algumas ficam fora das caixas verdes
2. **Linha amarela se estende demais** - não fica restrita ao braço

## Soluções implementadas:

### 1. Filtro de confiança
- Adicionado parâmetro `min_confidence=0.4` no `calc_axis()`
- Filtra detecções fracas que podem ser falsos positivos

### 2. Linha restrita ao braço
- Se `neck` (braço) for detectado, a linha fica limitada aos bounds do braço
- Caso contrário, usa uma linha mais curta (1/3 da imagem)

### 3. Melhorias sugeridas para o treinamento YOLO:

#### A. Data Augmentation
```python
# No treinamento, adicionar mais variações:
augmentations = {
    'brightness': 0.3,
    'contrast': 0.3,
    'rotation': 5,  # graus
    'scale': 0.2,
    'perspective': 0.0002
}
```

#### B. Ajustar anchors e NMS
```python
# No modelo YOLO
model = YOLO('yolov8n.pt')
model.train(
    data='seu_dataset.yaml',
    epochs=100,
    imgsz=640,
    conf=0.25,        # threshold de confiança mais baixo
    iou=0.45,         # threshold de IoU para NMS
    max_det=50,       # máximo de detecções por imagem
)
```

#### C. Post-processing inteligente
```python
def filter_frets_by_geometry(frets, neck):
    """Filtra trastes baseado na geometria do braço"""
    if not neck:
        return frets
    
    neck_x, neck_y, neck_w, neck_h = neck[0][:4]
    
    # Filtra trastes que estão dentro do braço
    valid_frets = []
    for fx, fy, conf in frets:
        # Verificar se está dentro dos limites do braço
        if (neck_x <= fx <= neck_x + neck_w and 
            neck_y <= fy <= neck_y + neck_h):
            valid_frets.append((fx, fy, conf))
    
    return valid_frets
```

### 4. Técnicas para melhorar detecção:

#### A. Múltiplas escalas
- Treinar com imagens de diferentes resoluções
- Usar TTA (Test Time Augmentation) na inferência

#### B. Ensemble de modelos
- Treinar múltiplos modelos e combinar predições
- Usar diferentes arquiteturas (YOLOv8n, YOLOv8s, YOLOv8m)

#### C. Pós-processamento baseado em padrões
- Trastes seguem um padrão geométrico regular
- Implementar validação baseada em espaçamento esperado

### 5. Implementação prática:

```python
def improve_fret_detection(results, frame):
    # 1. Filtrar por confiança
    frets = [f for f in results['frets'] if f[2] > 0.3]
    
    # 2. Ordenar por posição Y (da pestana para baixo)
    frets.sort(key=lambda x: x[1])
    
    # 3. Filtrar outliers baseado em espaçamento
    if len(frets) >= 3:
        # Calcular espaçamentos
        spacings = [frets[i+1][1] - frets[i][1] for i in range(len(frets)-1)]
        median_spacing = sorted(spacings)[len(spacings)//2]
        
        # Remover trastes com espaçamento muito diferente
        filtered = [frets[0]]  # sempre manter a primeira
        for i in range(1, len(frets)):
            spacing = frets[i][1] - filtered[-1][1]
            if 0.5 * median_spacing <= spacing <= 2.0 * median_spacing:
                filtered.append(frets[i])
        
        return filtered
    
    return frets
```
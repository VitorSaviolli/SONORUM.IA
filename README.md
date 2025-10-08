# Yolo_guitar

Sistema de detecção e análise de violão usando YOLO.

## Estrutura do Projeto

```
Yolo_guitar/
├── src/                      # Código-fonte principal
│   ├── modules/              # Módulos auxiliares
│   │   ├── __init__.py
│   │   ├── calc_axis.py      # Cálculo do eixo do instrumento
│   │   ├── collect_data.py   # Coleta de dados das detecções
│   │   └── draw_boxes.py     # Desenho de caixas e elementos
│   ├── __init__.py
│   └── main.py               # Script principal
├── runs/                     # Resultados de treinamento/detecção YOLO
│   └── detect/
│       └── train/
│           └── weights/
│               └── best.onnx # Modelo treinado
├── IA/                       # Exemplos e experimentos
├── violao.jpg                # Imagem de teste
├── pyproject.toml            # Dependências Poetry
├── poetry.lock               # Lock de dependências
└── README.md                 # Este arquivo

```

## O que vai em cada pasta

### `src/` - Código-fonte
- **O que vai aqui:** Todo o código Python da aplicação
- **Estrutura:**
  - `main.py`: ponto de entrada da aplicação
  - `modules/`: módulos auxiliares reutilizáveis
  - `__init__.py`: torna `src` um pacote Python

### `runs/` - Resultados do YOLO
- **O que vai aqui:** Outputs de treinamento, pesos do modelo, métricas
- **Gerado automaticamente** pelo Ultralytics YOLO

### Raiz do projeto
- **O que vai aqui:**
  - `pyproject.toml`, `poetry.lock`: gerenciamento de dependências
  - `README.md`: documentação
  - Imagens de teste (`violao.jpg`)
  - `.git/`: controle de versão
  - Arquivos de configuração (`.gitignore`, etc.)

## Como executar

### 1. Instalar dependências

```bash
# Na raiz do projeto (Yolo_guitar/)
poetry install
```

### 2. Rodar a aplicação

**Opção A: Da raiz do projeto (recomendado)**
```bash
poetry run python -m src.main
```

**Opção B: De dentro da pasta src**
```bash
cd src
poetry run python main.py
```

## Teclas de atalho (durante execução)

- `q`: Sair da aplicação
- `1`: Mostrar tudo (frets, frets_box, nut, axis)
- `2`: Apenas trastes (frets, frets_box, projections, mean_frets)
- `3`: Apenas projeção (projections)
- `4`: Projeção comparado a centroides (projections, frets)
- `5`: Mostrar tudo (sem filtros)

## Modo webcam vs. imagem

- **Webcam (padrão):** Descomente as linhas de `cap.read()` no `main.py`
- **Imagem estática:** Deixe `frame = cv2.imread("../violao.jpg")` ativo

## Requisitos

- Python 3.10+
- Poetry
- OpenCV (`opencv-python`)
- Ultralytics YOLO
- Dependências listadas em `pyproject.toml`

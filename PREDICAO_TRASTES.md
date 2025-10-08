# 🎸 Predição de Trastes - Yolo_guitar

## 🎯 Funcionalidade Implementada

A nova função `predict_frets_positions` usa o eixo calculado (`calc_axis`) para prever posições de trastes com base na **teoria musical** e **geometria do violão**.

## 🔧 Como Funciona

### 1. **Análise do Eixo**
- Usa `calc_axis` para mapear o eixo central do braço
- Calcula ângulo e direção baseado na pestana (nut) e trastes detectadas

### 2. **Geometria Musical**
- Aplica a fórmula musical: `distância = escala × (1 - 2^(-traste/12))`
- Usa a razão áurea entre trastes (12ª raiz de 2 ≈ 1.059463)

### 3. **Combinação Inteligente**
- **Trastes detectadas:** círculos verdes (alta confiança do YOLO)
- **Trastes previstas:** círculos azuis (baseadas em geometria)
- **Filtro geométrico:** remove detecções com espaçamento anômalo

## 🎮 Novos Controles (Teclas)

| Tecla | Função | Visualização |
|-------|--------|--------------|
| `1` | TUDO | frets, frets_box, nut, axis |
| `2` | APENAS TRASTES | frets, frets_box, projections, mean_frets |
| `3` | APENAS PROJEÇÃO | projections |
| `4` | PROJEÇÃO + CENTROIDES | projections, frets |
| `5` | SEM FILTROS | Mostra tudo |
| `6` | **APENAS PREDIÇÕES** | predicted_frets, axis |
| `7` | **DETECTADAS + PREDITAS** | frets, predicted_frets, axis |
| `8` | **ANÁLISE COMPLETA** | frets, predicted_frets, axis, projections, nut |
| `q` | SAIR | - |

## 🎨 Código Visual

### Cores e Significados:
- 🟢 **Verde:** Trastes detectadas pelo YOLO
- 🔵 **Azul:** Trastes previstas por geometria
- 🟡 **Amarelo:** Eixo do violão (limitado ao braço)
- 🔴 **Vermelho:** Pestana (nut)
- 🟠 **Laranja:** Projeções no eixo

## 📊 Melhorias Implementadas

### 1. **Filtro Geométrico**
```python
improve_fret_detection_with_geometry(data, axis_info)
```
- Remove trastes com espaçamento anômalo
- Usa mediana dos espaçamentos como referência
- Mantém apenas trastes com padrão regular

### 2. **Predição Baseada em Teoria**
```python
predict_frets_positions(frame, data, num_frets=12)
```
- Calcula 12 trastes baseado na escala musical
- Evita sobreposição com trastes detectadas
- Alta confiança (0.85) para previsões teóricas

### 3. **Visualização Inteligente**
- Números dos trastes nas previsões (`F1`, `F2`, etc.)
- Bordas destacadas para diferenciação
- Controles granulares de visualização

## 🚀 Como Usar

### 1. **Executar com Predições**
```powershell
cd C:\Users\vitor\OneDrive\Área de Trabalho\faculdade\sonorum\Yolo_guitar\src
poetry run python main.py
```

### 2. **Testar Diferentes Modos**
- Pressione `6`: Ver apenas predições
- Pressione `7`: Ver detectadas + preditas
- Pressione `8`: Análise completa

### 3. **Ajustar Parâmetros**
No `main.py`, você pode alterar:
```python
predicted_data = predict_frets_positions(frame, improved_data, 
                                        num_frets=15,  # mais trastes
                                        draw=True)
```

## 🎯 Benefícios

### ✅ **Maior Precisão**
- Combina detecção com geometria teórica
- Preenche trastes não detectadas pelo YOLO
- Remove falsos positivos

### ✅ **Robustez**
- Funciona mesmo com detecções parciais
- Adaptável a diferentes escalas de violão
- Fallbacks seguros quando dados são limitados

### ✅ **Visualização Rica**
- Diferentes modos de visualização
- Informações claras (números dos trastes)
- Cores intuitivas

## 🔧 Configurações Avançadas

### Ajustar Sensibilidade
```python
# Em main.py, linha da predição:
axis = calc_axis(frame, data['nut'], data['frets'], 
                 neck=data.get('neck'), neck_box=data.get('neck_box'),
                 draw=False, min_confidence=0.3)  # era 0.4
```

### Mais Trastes
```python
predicted_data = predict_frets_positions(frame, improved_data, 
                                        num_frets=18)  # violão com 18 trastes
```

### Desabilitar Desenho Automático
```python
predicted_data = predict_frets_positions(frame, improved_data, 
                                        draw=False)  # só calcular
```

## 🧪 Teste e Validação

1. **Execute o programa**
2. **Pressione `8`** para ver análise completa
3. **Compare** trastes azuis (previstas) com verdes (detectadas)
4. **Use `6`** para ver apenas predições e avaliar precisão
5. **Teste com diferentes imagens** de violão

## 📈 Próximas Melhorias

- [ ] Detecção automática do tipo de violão (clássico/folk/elétrico)
- [ ] Calibração automática da escala
- [ ] Predição de cordas (não apenas trastes)
- [ ] Exportar coordenadas para análise externa
- [ ] Interface gráfica para ajustes em tempo real
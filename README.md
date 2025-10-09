# Detector de Acordes em Tempo Real

Este projeto processa áudio em tempo real para identificar acordes de violão. Ele captura o som do microfone, analisa as frequências e compara com uma biblioteca de referência para exibir o acorde na tela.

---

## Estrutura do Projeto (backend)

- **`src/`**: Código-fonte.
  - `ui/`: Lógica da interface gráfica.
  - `processing/`: Lógica para processar e analisar áudio em tempo real.
  - `comparison/`: Lógica para comparar e identificar acordes.
- **`data/`**: Armazena os arquivos de áudio (`.wav`) dos acordes de referência.
- **`config/`**: Arquivos de configuração.

## Dependências

O gerenciamento de dependências deste projeto é feito com Poetry.

## Por que usar o Poetry?

Poetry é uma ferramenta que gerencia dependências e ambientes virtuais. Ele garante que o projeto funcione de forma consistente para todos, pois todas as bibliotecas e suas versões são listadas no arquivo pyproject.toml.

Para instalar o Poetry, use o pip:

`pip install poetry`

Após a instalação, use o seguinte comando no diretório do projeto para instalar todas as dependências:

`poetry install`
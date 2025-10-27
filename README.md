# UNIBRASIL Surveyor - Otimizador de Roteiro de Drone

Sistema de otimização de roteiro para drone autônomo usando algoritmo genético híbrido para mapear CEPs em Curitiba.

## Características

- **Algoritmo Genético Híbrido** com estratégia do vizinho mais próximo
- Cálculo de distância usando fórmula de Haversine
- Modelo meteorológico com dados de vento
- Gestão de autonomia baseada na velocidade
- Validação robusta de soluções
- Visualização de rotas otimizadas
- Geração de relatórios em CSV
- Sistema de IDs fictícios para otimização de memória

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Crie um ambiente virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

### Executar Otimização
```bash
python main.py
```
### Executar Testes
```bash
# simples
pytest

# Mostra cada teste
pytest -v

# Com saída do print
pytest -s

# Teste específico
pytest tests/test_calculations.py
```
## Estrutura do Projeto

```
unibrasil-surveyor/
├── src/                   # Código fonte modular
│   ├── core/              # Módulos principais
│   ├── algorithms/        # Algoritmo genético 
│   ├── utils/             # Utilitários
│   └── visualization/     # Visualização
├── data/                  # Dados dos CEPs
├── output/                # Arquivos gerados
├── main.py                # Script principal
└── requirements.txt       # Dependências
```

## Arquivos Gerados

- `output/roteiro_otimizado_DDMMHHMMSS.csv`: Rota otimizada em formato CSV
- `output/roteiro_visualizacao_DDMMHHMMSS.png`: Visualização gráfica da rota

## Requisitos do Sistema

- Python 3.7+
- Bibliotecas: numpy, matplotlib, pytest, tqdm

## Autor

Desenvolvido para o projeto UNIBRASIL Surveyor - Serviços Cognitivos
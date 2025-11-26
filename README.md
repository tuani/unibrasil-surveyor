# UNIBRASIL Surveyor - Gerador de Roteiro de Drone

Sistema de geração de roteiro para drone autônomo usando algoritmo genético híbrido com heurística de vizinho mais próximo para mapear CEPs em Curitiba.

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

### Executar Geração de Rota
```bash
python main.py
```

O sistema irá gerar uma rota otimizada e salvar:
- Arquivo CSV com detalhes da rota
- Imagem PNG com visualização da rota

### Executar Testes
```bash
# Execução simples
pytest

# Modo verboso (mostra cada teste)
pytest -v

# Com saída dos prints (recomendado para debug)
pytest -s

# Teste específico
pytest tests/test_calculations.py
```

**Nota:** Use `pytest -s` para ver prints informativos durante a execução dos testes.
## Estrutura do Projeto

```
unibrasil-surveyor/
├── src/                   # Código fonte modular
│   ├── core/              # Módulos principais
│   │   ├── drone_optimizer.py    # GerenciadorRota (orquestrador)
│   │   ├── cost_calculator.py    # Cálculo de custos
│   │   └── validator.py          # Validação de rotas
│   ├── algorithms/        # Algoritmo genético 
│   │   └── genetic_algorithm.py  # Algoritmo genético híbrido
│   ├── utils/             # Utilitários
│   │   ├── calculations.py       # Cálculos geográficos e 2-opt
│   │   ├── data_manager.py       # Gerenciamento de dados
│   │   ├── id_mapper.py          # Mapeamento CEP ↔ ID
│   │   └── report_generator.py  # Geração de relatórios
│   └── visualization/     # Visualização
│       └── route_plotter.py       # Plotagem de rotas
├── data/                  # Dados dos CEPs
├── output/                # Arquivos gerados
├── tests/                 # Testes unitários
├── main.py                # Script principal
└── requirements.txt       # Dependências
```

## Arquivos Gerados

- `output/roteiro_DDMMHHMMSS.csv`: Rota gerada em formato CSV com detalhes de cada trecho
- `output/roteiro_visualizacao_DDMMHHMMSS.png`: Visualização gráfica da rota no mapa

## Requisitos do Sistema

- Python 3.7+
- Bibliotecas: numpy, matplotlib, pytest, tqdm

## Autor

Desenvolvido para o projeto UNIBRASIL Surveyor - Serviços Cognitivos
# FarmTech Solutions

**🎥 [Vídeo Demonstrativo](https://youtu.be/LlLFZXPC-bU)**

Plataforma completa de agricultura de precisão integrando análise de dados, IoT, machine learning, visão computacional e computação em nuvem.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

# FIAP - Faculdade de Informática e Administração Paulista

[![FIAP - Faculdade de Informática e Administração Paulista](assets/logo-fiap.png)](https://www.fiap.com.br/)

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/yan-cotta/">Yan Cotta</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi</a>

## Sobre o Projeto

Sistema desenvolvido como projeto final do programa de Engenharia de IA da FIAP, combinando seis módulos principais para otimização de produção agrícola através de dados e inteligência artificial.

### Objetivos

- Otimizar consumo de água com irrigação preditiva
- Reduzir perdas de culturas com detecção precoce de pragas
- Maximizar ROI através de algoritmo genético de alocação
- Gerar insights acionáveis a partir de múltiplas fontes de dados

## Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│              Dashboard Unificado (Streamlit)                  │
│         Interface de Análise e Controle em Tempo Real         │
├──────────────────────────────────────────────────────────────┤
│ Análise R │  Database  │   IoT     │    ML     │  Cloud      │
│           │  Layer     │  ESP32    │  Pipeline │  AWS        │
├──────────────────────────────────────────────────────────────┤
│     Visão Computacional     │   Motor de Otimização          │
│      (YOLOv5 + LLM)        │   (Algoritmo Genético)         │
└──────────────────────────────────────────────────────────────┘
```

## Funcionalidades

### 1. Análise de Dados Agrícolas
Análise estatística de dados de produção agrícola brasileira com visualizações interativas em Plotly.

### 2. Banco de Dados Corporativo
- SQLAlchemy 2.0 ORM com migrações Alembic
- Arquitetura agnóstica (SQLite/PostgreSQL/MySQL)
- Três tabelas normalizadas: irrigação, sensores, detecção de pragas

### 3. Rede de Sensores IoT
- Arquitetura distribuída baseada em ESP32
- Monitoramento: umidade do solo, pH, níveis NPK
- Controle automatizado de irrigação via relé
- 20 sensores simulados na região de Ribeirão Preto

### 4. Pipeline de Machine Learning
- Classificador Random Forest (98,5% de acurácia)
- 4 features: umidade, pH, fósforo, potássio
- Persistência via joblib
- Interface de predição em tempo real

### 5. Infraestrutura em Nuvem
- Arquitetura AWS com análise de custos
- Sistema de alertas via SNS com failover automático
- Modo simulação para ambientes de desenvolvimento
- Severidades: INFO, WARNING, CRITICAL, EMERGENCY

### 6. Sistema de Visão Computacional
Arquitetura dupla:
- **Modelo FarmTech**: YOLOv5 customizado (mAP@0.5: 51,3%)
- **YOLOv5s Geral**: Pré-treinado em COCO (80 classes)
- IA Híbrida: Detecção edge (YOLO) + Análise cloud (GPT-4o Vision)

### 7. Interface em Linguagem Natural
- Chatbot OpenAI para consultas ao banco de dados
- Respostas contextuais com dados recentes de sensores
- Análise estatística em linguagem natural

### 8. Otimizador com Algoritmo Genético
- Resolução do problema da mochila binária para seleção de culturas
- População, gerações e taxas de crossover/mutação configuráveis
- Visualização interativa da evolução do fitness

## Stack Tecnológica

### Backend & Data Science
- Python 3.12.3
- Pandas 2.2.3
- NumPy 2.1.3
- Scikit-learn 1.5.2
- PyTorch 2.5.1
- SQLAlchemy 2.0.23
- Alembic 1.13.1

### Visão Computacional
- Ultralytics 8.3.29
- OpenCV
- Pillow 10.4.0
- OpenAI Vision API

### Visualização & UI
- Streamlit 1.39.0
- Plotly 5.24.1
- Matplotlib 3.9.2

### Cloud & Infraestrutura
- AWS Boto3 1.35.67
- Requests 2.32.3
- Python-dotenv 1.0.1

## Instalação

### Pré-requisitos

- Python 3.12 ou superior
- pip
- Git
- 8GB RAM mínimo
- 2GB espaço em disco

### Passos

1. Clone o repositório
```bash
git clone https://github.com/seu-org/FarmTech_System.git
cd FarmTech_System
```

2. Crie um ambiente virtual
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Inicialize o banco de dados
```bash
cd fase_2_database_design
python database_manager.py
```

5. Configure variáveis de ambiente (opcional)
```bash
# Para integração AWS
export AWS_ACCESS_KEY_ID=<sua_chave>
export AWS_SECRET_ACCESS_KEY=<sua_secret>
export AWS_DEFAULT_REGION=us-east-1

# Para recursos de LLM
export OPENAI_API_KEY=<sua_chave_openai>
```

## Como Usar

### Executar o Dashboard

```bash
streamlit run app_integrated.py
```

Acesse em `http://localhost:8501`

### Navegação no Dashboard

- **Visão Geral**: Arquitetura do sistema e métricas
- **Fase 1**: Análise de dados agrícolas
- **Fase 2**: Visualização do esquema do banco de dados
- **Fase 3**: Mapa da rede de sensores IoT
- **Fase 4**: Interface de predição ML
- **Fase 5**: Análise de custos AWS e alertas
- **Fase 6**: Detecção de visão computacional
- **Otimizador Genético**: Alocação de recursos
- **Assistente IA**: Consultas em linguagem natural

### Executar Módulos Standalone

```bash
# Treinar modelo ML
cd fase_4_dashboard_ml/scripts
python train_model.py

# Testar otimizador genético
cd ir_alem_2_genetic_algorithm
python genetic_optimizer.py

# Executar migrações de banco
cd fase_2_database_design
alembic upgrade head
```

## Estrutura do Projeto

```
FarmTech_System/
├── app_integrated.py              # Dashboard principal
├── requirements.txt               # Dependências Python
├── README.md                      # Este arquivo
├── LICENSE                        # Licença MIT
│
├── fase_1_R_analysis/            # Análise de dados
│   ├── data/agro_data.csv
│   └── src/analise_agro.R
│
├── fase_2_database_design/       # Camada de banco de dados
│   ├── database_manager.py
│   ├── alembic.ini
│   └── migrations/
│
├── fase_3_iot_esp32/             # Firmware IoT
│   ├── prog1.ino
│   └── diagram.json
│
├── fase_4_dashboard_ml/          # Pipeline ML
│   ├── irrigation_model.joblib
│   └── scripts/
│
├── fase_5_aws_docs/              # Documentação cloud
│   └── docs/
│
├── fase_6_vision_yolo/           # Visão computacional
│   ├── best.pt
│   └── report.md
│
└── ir_alem_2_genetic_algorithm/  # Motor de otimização
    ├── genetic_optimizer.py
    └── README_GENETIC_OPTIMIZER.md
```

## Módulos

### Fase 1: Análise de Dados Agrícolas
Análise estatística da produção agrícola brasileira com visualizações Plotly interativas.

### Fase 2: Design de Banco de Dados
Arquitetura de banco de dados corporativa com SQLAlchemy ORM e migrações Alembic.

### Fase 3: Rede de Sensores IoT
Sistema de monitoramento distribuído baseado em ESP32 com aquisição de dados em tempo real.

### Fase 4: Pipeline de Machine Learning
Classificador Random Forest para predição de irrigação com recursos de IA explicável.

### Fase 5: Infraestrutura em Nuvem
Design de arquitetura AWS com sistema de alertas SNS e análise de otimização de custos.

### Fase 6: Visão Computacional
Sistema de visão IA híbrida combinando detecção edge e inteligência cloud.

## Recursos Avançados

### Otimização com Algoritmo Genético

Resolve o problema da mochila binária para seleção ótima de culturas dentro das restrições de orçamento.

**Configuração:**
```python
optimizer = FarmGeneticOptimizer(
    items_df=crops_dataframe,
    budget=150_000,
    population_size=32,
    num_generations=1000,
    crossover_rate=0.8,
    mutation_rate=0.15
)
```

### Interface em Linguagem Natural

Chatbot OpenAI com análise de dados agrícolas contextual.

**Exemplos de Consultas:**
- "Qual é a umidade média do solo?"
- "Quantos sensores indicam necessidade crítica de irrigação?"
- "Identifique áreas com pH fora da faixa ideal (6.0-7.5)"

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autores

**Yan Pimentel Cotta** - RM562836  
Programa de Engenharia de IA FIAP

---

**FarmTech Solutions** | Plataforma de Agricultura de Precisão  
© 2025 FarmTech Solutions. Todos os direitos reservados.

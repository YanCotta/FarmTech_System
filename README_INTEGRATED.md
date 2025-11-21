# 🌾 FarmTech Solutions - Sistema Integrado de Agritech com IA

Sistema completo de agricultura de precisão que integra análise de dados, IoT, Machine Learning, Visão Computacional e Cloud Computing para otimizar a produção agrícola.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Fases do Projeto](#-fases-do-projeto)
- [Desafios "Ir Além"](#-desafios-ir-além)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🌟 Sobre o Projeto

O **FarmTech Solutions** é um sistema completo de agricultura de precisão desenvolvido como parte do curso de IA da FIAP. O projeto integra 6 fases principais e 2 desafios extras, abrangendo desde análise de dados até visão computacional e otimização com algoritmos genéticos.

### Objetivos Principais

- 🌱 **Aumentar a eficiência** no uso de recursos hídricos
- 📊 **Reduzir perdas** causadas por pragas e doenças
- 🧬 **Otimizar alocação** de recursos agrícolas
- 📈 **Prover insights** baseados em dados e IA

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                 Dashboard Integrado                      │
│                   (Streamlit)                            │
├─────────────────────────────────────────────────────────┤
│  Fase 1   │  Fase 2   │  Fase 3   │  Fase 4   │ Fase 5 │
│  Dados R  │    DB     │   IoT     │    ML     │   AWS  │
├─────────────────────────────────────────────────────────┤
│           Fase 6          │      Ir Além 1 & 2          │
│      Visão YOLO           │    AWS + Genético           │
└─────────────────────────────────────────────────────────┘
```

## ✨ Funcionalidades

### Módulos Principais

1. **📊 Análise de Dados (R)**
   - Processamento de dados agrícolas
   - Estatísticas descritivas
   - Visualizações interativas

2. **🗄️ Banco de Dados**
   - Modelo relacional completo
   - Armazenamento de sensores e irrigação
   - Histórico de detecções

3. **🔌 IoT com ESP32**
   - Monitoramento em tempo real
   - Sensores de umidade, pH e nutrientes
   - Acionamento automático de bomba

4. **🤖 Machine Learning**
   - Predição de necessidade de irrigação
   - Random Forest otimizado
   - Explicabilidade (XAI)

5. **☁️ Infraestrutura AWS**
   - Análise de custos
   - Sistema de alertas SNS
   - Simulação para desenvolvimento

6. **👁️ Visão Computacional**
   - Detecção de pragas com YOLOv5
   - Upload e análise de imagens
   - Alertas automáticos

7. **🧬 Otimização Genética**
   - Alocação ótima de recursos
   - Algoritmo genético customizado
   - Visualização de evolução

## 🛠️ Tecnologias

### Backend & Data Science
- **Python 3.10+**
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Scikit-learn** - Machine Learning
- **PyTorch** - Deep Learning

### Visão Computacional
- **YOLOv5 (Ultralytics)** - Detecção de objetos
- **OpenCV** - Processamento de imagens
- **Pillow** - Manipulação de imagens

### Interface & Visualização
- **Streamlit** - Dashboard interativo
- **Matplotlib** - Gráficos estáticos
- **Seaborn** - Visualizações estatísticas
- **Plotly** - Gráficos interativos

### Cloud & IoT
- **AWS Boto3** - Integração com AWS
- **ESP32** - Microcontrolador IoT
- **Arduino** - Firmware IoT

### Banco de Dados
- **SQLite** - Armazenamento local
- **SQL** - Queries e operações

## 📦 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/FarmTech_System.git
cd FarmTech_System
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente (opcional)**
```bash
# Para usar AWS real (caso contrário, modo simulação será usado)
export AWS_ACCESS_KEY_ID=sua_chave
export AWS_SECRET_ACCESS_KEY=sua_chave_secreta
export AWS_DEFAULT_REGION=us-east-1
```

5. **Prepare o banco de dados (opcional)**
```bash
cd fase_4_dashboard_ml/scripts
python populate_db.py
```

## 🚀 Como Usar

### Executar o Dashboard Integrado

```bash
# Na raiz do projeto
streamlit run app_integrated.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

### Navegação

Use o menu lateral para navegar entre as fases:

- **🏠 Home**: Visão geral do projeto
- **📊 Fase 1**: Análise de dados agrícolas
- **🗄️ Fase 2**: Visualização do modelo de dados
- **🔌 Fase 3**: Código e configuração IoT
- **🤖 Fase 4**: Predições com Machine Learning
- **☁️ Fase 5**: AWS e sistema de alertas
- **👁️ Fase 6**: Detecção de objetos com YOLO
- **🧬 Ir Além 2**: Otimização genética

### Executar Módulos Individuais

```bash
# Treinar modelo de ML
cd fase_4_dashboard_ml/scripts
python train_model.py

# Testar otimizador genético
python genetic_optimizer.py

# Testar AWS Manager
python aws_manager.py

# Dashboard original da Fase 4
streamlit run dashboard.py
```

## 📁 Estrutura do Projeto

```
FarmTech_System/
├── app_integrated.py              # Dashboard principal integrado
├── requirements.txt               # Dependências do projeto
├── README.md                      # Este arquivo
├── LICENSE                        # Licença MIT
│
├── fase_1_R_analysis/            # Fase 1: Análise com R
│   ├── data/
│   │   └── agro_data.csv         # Dados agrícolas
│   └── src/
│       └── analise_agro.R        # Script R
│
├── fase_2_database_design/       # Fase 2: Banco de Dados
│   └── docs/
│       ├── DER_FarmTech.pdf      # Documentação DER
│       └── der_farmtech_solutions.png
│
├── fase_3_iot_esp32/             # Fase 3: IoT ESP32
│   ├── prog1.ino                 # Firmware Arduino
│   ├── diagram.json              # Configuração Wokwi
│   ├── platformio.ini            # Configuração PlatformIO
│   └── wokwi.toml               # Config Wokwi
│
├── fase_4_dashboard_ml/          # Fase 4: ML Dashboard
│   ├── irrigation_model.joblib   # Modelo treinado
│   ├── irrigation.db             # Banco SQLite
│   ├── scripts/
│   │   ├── dashboard.py          # Dashboard original
│   │   ├── database.py           # Operações DB
│   │   ├── train_model.py        # Treinamento ML
│   │   ├── utils.py              # Utilitários
│   │   ├── populate_db.py        # Populador DB
│   │   ├── verify_db.py          # Verificador DB
│   │   ├── weather_integration.py
│   │   ├── genetic_optimizer.py  # 🆕 Algoritmo Genético
│   │   ├── aws_manager.py        # 🆕 Gerenciador AWS
│   │   └── requirements.txt
│   └── tests/
│       └── test_utils.py
│
├── fase_5_aws_docs/              # Fase 5: AWS
│   └── docs/
│       ├── README.md
│       ├── aws_baseline_cost.png
│       └── aws_comparison_cost.png
│
├── fase_6_vision_yolo/           # Fase 6: YOLO
│   ├── best.pt                   # Modelo YOLO treinado
│   ├── last.pt
│   ├── report.md
│   ├── Entrega2_RaphaelDaSilva_RM561452_fase6_cap1.ipynb
│   ├── entregavel_1_fase6_cap1.ipynb
│   └── ir_alem_opcao_2_fase_6_cap1.ipynb
│
└── ir_alem_2_genetic_algorithm/  # Algoritmo Genético
    └── TIAO_ON_RN_Aula6.ipynb
```

## 📚 Fases do Projeto

### Fase 1: Análise de Dados com R 📊
Análise estatística de dados agrícolas do Brasil, incluindo:
- Produção por estado
- Área plantada
- Classificação de produtividade
- Visualizações interativas

### Fase 2: Design de Banco de Dados 🗄️
Modelagem completa do banco de dados relacional:
- Diagrama Entidade-Relacionamento (DER)
- Tabelas: Fazendas, Culturas, Sensores, Irrigação, Pragas
- Relacionamentos e constraints

### Fase 3: IoT com ESP32 🔌
Sistema de monitoramento e controle automatizado:
- Sensores: DHT22 (umidade), pH, nutrientes
- Acionamento de bomba via relé
- Display LCD para visualização
- Comunicação serial

### Fase 4: Machine Learning Dashboard 🤖
Predição inteligente de irrigação:
- Random Forest otimizado com GridSearch
- 4 features: umidade, pH, fósforo, potássio
- Acurácia: 98.5%
- Explicabilidade (feature importance)

### Fase 5: Infraestrutura AWS ☁️
Análise de custos e planejamento cloud:
- Comparação de arquiteturas
- Estimativa de custos
- Serviços: EC2, S3, RDS, SNS

### Fase 6: Visão Computacional 👁️
Detecção de objetos com YOLOv5:
- Treinamento customizado
- Detecção de pragas
- Upload de imagens
- Integração com alertas

## 🏆 Desafios "Ir Além"

### Ir Além 1: Sistema de Mensageria AWS 📤

Implementação de alertas via AWS SNS com fallback de simulação:

**Funcionalidades:**
- Envio de alertas para tópicos SNS
- Simulação automática quando AWS não configurado
- Três tipos de alertas:
  - 💧 Umidade do solo baixa
  - 🐛 Detecção de pragas
  - 🔔 Alertas genéricos do sistema
- Níveis de severidade: INFO, WARNING, CRITICAL, EMERGENCY

**Uso:**
```python
from fase_4_dashboard_ml.scripts.aws_manager import AWSManager, AlertLevel

manager = AWSManager()

# Alerta de umidade
manager.send_soil_moisture_alert(humidity=25.0, threshold=30.0)

# Alerta de praga
manager.send_pest_detection_alert(
    pest_type="Lagarta",
    confidence=85.5,
    location="Setor B"
)
```

### Ir Além 2: Otimização com Algoritmo Genético 🧬

Implementação de algoritmo genético para otimizar alocação de recursos:

**Funcionalidades:**
- Problema da mochila binária aplicado à agricultura
- Seleção ótima de culturas dentro do orçamento
- Visualização da evolução do fitness
- Configuração de parâmetros (população, gerações, taxas)

**Algoritmo:**
1. **Fitness**: Maximiza valor total respeitando orçamento
2. **Seleção**: Elitismo (melhores indivíduos)
3. **Crossover**: Um ponto com taxa configurável
4. **Mutação**: Flip de bits com taxa configurável

**Uso:**
```python
from fase_4_dashboard_ml.scripts.genetic_optimizer import (
    FarmGeneticOptimizer, 
    generate_sample_farm_items
)

# Gera culturas de exemplo
items_df = generate_sample_farm_items(num_items=20)

# Cria otimizador
optimizer = FarmGeneticOptimizer(
    items_df=items_df,
    budget=150,
    population_size=16,
    num_generations=500
)

# Executa otimização
selected_items, total_value, total_cost, history = optimizer.optimize()

# Plota evolução
fig = optimizer.plot_fitness_evolution()
```

## 🧪 Testes

```bash
# Executar testes unitários
cd fase_4_dashboard_ml
pytest tests/

# Executar com cobertura
pytest --cov=scripts tests/
```

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Raphael da Silva** - RM561452 - [GitHub](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- FIAP - Faculdade de Informática e Administração Paulista
- Professores do curso de IA
- Comunidade open source

## 📞 Contato

- **Email**: contato@farmtech.com
- **Website**: www.farmtech.com
- **LinkedIn**: [FarmTech Solutions](https://linkedin.com/company/farmtech)

---

<div align="center">
  <p><strong>🌾 FarmTech Solutions</strong></p>
  <p>Desenvolvido com ❤️ para a agricultura do futuro</p>
  <p>© 2024 FarmTech Solutions. Todos os direitos reservados.</p>
</div>

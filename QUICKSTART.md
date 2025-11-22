# FarmTech Solutions - Guia de Início Rápido

Instruções passo a passo para executar a plataforma FarmTech Solutions em minutos.

## Início Rápido (5 Minutos)

### 1. Instalação

```bash
# Clonar repositório
git clone https://github.com/seu-org/FarmTech_System.git
cd FarmTech_System

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Inicializar Banco de Dados

```bash
cd fase_2_database_design
python database_manager.py
cd ..
```

### 3. Executar Dashboard

```bash
streamlit run app_integrated.py
```

Acesse em: **http://localhost:8501**

---

## Tutoriais dos Módulos

### Fase 1: Análise de Dados Agrícolas

1. Navegue até "Fase 1: Análise de Dados" na barra lateral
2. Revise as estatísticas de produção agrícola brasileira
3. Interaja com as visualizações Plotly (hover, zoom, pan)
4. Exporte datasets via botões de download CSV

**Insights Principais:**
- Top 10 estados por produção
- Distribuição de classificação de produtividade
- Correlação área vs produção

### Fase 3: Rede de Sensores IoT

1. Selecione "Fase 3: IoT ESP32"
2. Explore o mapa interativo de sensores (região de Ribeirão Preto)
3. Identifique sensores críticos (marcadores vermelhos = umidade < 30%)
4. Revise a tabela de status dos sensores
5. Baixe dados de sensores para análise externa

**Recursos do Mapa:**
- 20 sensores distribuídos geograficamente
- Status codificado por cores (verde=normal, vermelho=crítico)
- Tooltips com métricas detalhadas ao passar o mouse

### Fase 4: Predição com Machine Learning

1. Navegue até "Fase 4: Machine Learning"
2. Insira parâmetros do sensor:
   - Umidade: 25%
   - pH: 6.5
   - Fósforo: Presente
   - Potássio: Presente
3. Clique em "Obter Predição"
4. Revise a recomendação do modelo e pontuação de confiança

**Especificações do Modelo:**
- Algoritmo: Random Forest
- Acurácia: 98,5%
- Features: 4 (umidade, pH, P, K)

### Fase 5: Sistema de Alertas AWS

1. Selecione "Fase 5: AWS & Alertas"
2. Escolha o tipo de alerta (Umidade do Solo / Detecção de Pragas / Genérico)
3. Configure parâmetros do alerta
4. Clique em "Enviar Alerta"
5. Verifique entrega do alerta (modo simulação se AWS não configurado)

**Níveis de Severidade:**
- INFO: Atualizações de rotina
- WARNING: Atenção necessária
- CRITICAL: Ação imediata
- EMERGENCY: Falha do sistema

### Fase 6: Detecção de Visão Computacional

1. Navegue até "Fase 6: Visão Computacional"
2. Selecione modelo YOLO:
   - **Modelo FarmTech**: Detecção especializada de pragas
   - **YOLOv5s**: Detecção geral de objetos (80 classes)
3. Faça upload de imagem (JPG/PNG)
4. Revise resultados de detecção com bounding boxes
5. Opcional: Habilite LLM Vision para análise fitopatológica

**Fluxo de IA Híbrida:**
- Detecção Edge (YOLO): Localização rápida de objetos
- Inteligência Cloud (GPT-4o): Análise diagnóstica detalhada

### Otimização com Algoritmo Genético

1. Selecione "Otimização Genética"
2. Configure orçamento (ex: R$ 150.000)
3. Ajuste parâmetros do algoritmo:
   - Tamanho da população: 16-32
   - Gerações: 500-1000
   - Taxa de crossover: 0.7-0.9
   - Taxa de mutação: 0.1-0.2
4. Clique em "Gerar Dados de Culturas"
5. Clique em "Otimizar Recursos"
6. Analise culturas selecionadas e gráfico de evolução do fitness
7. Exporte resultados via download CSV

**Objetivo da Otimização:**
Maximizar valor das culturas respeitando restrições de orçamento (problema da mochila binária).

### Assistente IA (Interface em Linguagem Natural)

1. Navegue até "Assistente IA"
2. Insira chave API OpenAI (armazenada com segurança na sessão)
3. Selecione modelo (gpt-4o-mini recomendado)
4. Faça perguntas em linguagem natural:
   - "Qual é a umidade média do solo?"
   - "Quantos sensores requerem irrigação imediata?"
   - "Identifique setores com desequilíbrios de pH"
5. Revise respostas geradas pela IA com contexto estatístico

---

## Configuração Avançada

### Integração AWS

Habilite alertas SNS reais da AWS (em vez do modo simulação):

```bash
export AWS_ACCESS_KEY_ID=<sua_chave_acesso>
export AWS_SECRET_ACCESS_KEY=<sua_chave_secreta>
export AWS_DEFAULT_REGION=us-east-1
```

### Retreinar Modelo ML

```bash
cd fase_4_dashboard_ml/scripts
python train_model.py
```

### Operações de Banco de Dados

```bash
# Executar migrações
cd fase_2_database_design
alembic upgrade head

# Adicionar dados de seed
python database_manager.py
```

---

## Fluxos de Trabalho Comuns

### Fluxo 1: Suporte à Decisão de Irrigação

1. Navegue até Fase 4 (Predição ML)
2. Insira leituras atuais dos sensores
3. Obtenha recomendação de irrigação
4. Se irrigação necessária:
   - Mude para Fase 5 (Alertas AWS)
   - Envie alerta de umidade do solo
   - Acione sistema de irrigação automatizado

### Fluxo 2: Gerenciamento de Pragas

1. Navegue até Fase 6 (Visão Computacional)
2. Faça upload de imagem do campo
3. Aguarde resultados de detecção YOLO
4. Se praga detectada com confiança > 70%:
   - Clique em "Enviar Alerta AWS"
   - Revise confirmação do alerta
   - Inicie protocolo de controle de pragas

### Fluxo 3: Otimização de Orçamento

1. Navegue até Otimizador Genético
2. Defina orçamento disponível
3. Gere dataset de opções de culturas
4. Execute algoritmo de otimização
5. Revise culturas selecionadas (maximiza valor)
6. Exporte seleção para planejamento de compras

---

## Solução de Problemas

### Erros de Importação de Módulos

```bash
# Reinstalar dependências
pip install -r requirements.txt --upgrade --force-reinstall
```

### Arquivo de Modelo Não Encontrado

```bash
# Inicializar modelo
cd fase_4_dashboard_ml/scripts
python train_model.py
```

### Problemas ao Executar Dashboard

```bash
# Verificar diretório de trabalho
pwd  # Deve estar na raiz FarmTech_System

# Verificar instalação do Streamlit
streamlit --version

# Forçar reload
streamlit run app_integrated.py --server.port=8501
```

### Erros PyTorch/YOLO

```bash
# Instalar dependências de visão computacional
pip install torch torchvision ultralytics --upgrade
```

### Erros de Conexão com Banco de Dados

```bash
# Reinicializar banco de dados
cd fase_2_database_design
rm ../irrigation.db  # Remover banco antigo
python database_manager.py  # Criar banco novo
```

---

## Otimização de Performance

### Reduzir Tempo de Carregamento do Dashboard

1. Desabilite módulos não utilizados na barra lateral
2. Reduza contagem de sensores no mapa da Fase 3
3. Use tamanhos menores de imagem para uploads da Fase 6

### Otimizar Predições ML

1. Cache de carregamento de modelo (já implementado via `@st.cache_resource`)
2. Predições em lote para múltiplos sensores
3. Use quantização de modelo para deploy em produção

### Ajuste do Algoritmo Genético

- Aumente gerações (1000-2000) para melhores soluções
- População maior (32-64) melhora exploração
- Taxa de mutação menor (0.1) para ajuste fino
- Taxa de crossover maior (0.9) para convergência mais rápida

---

## Próximos Passos

Após completar o início rápido:

1. Revise [README.md](README.md) completo para detalhes de arquitetura
2. Explore [DATABASE_GUIDE.md](fase_2_database_design/docs/DATABASE_GUIDE.md) para documentação ORM
3. Estude [GENETIC_OPTIMIZER_SUMMARY.md](ir_alem_2_genetic_algorithm/GENETIC_OPTIMIZER_SUMMARY.md)
4. Personalize dashboards para casos de uso específicos
5. Integre com sistemas externos via API

---

## Melhores Práticas

- Use `Ctrl + Shift + R` para recarregar dashboard sem reiniciar
- Habilite ferramentas de desenvolvedor do navegador para monitorar performance
- Exporte dados regularmente para backup e análise externa
- Teste integração AWS em ambiente de desenvolvimento primeiro
- Valide detecções YOLO com LLM Vision para decisões críticas
- Documente configurações personalizadas em arquivos README separados

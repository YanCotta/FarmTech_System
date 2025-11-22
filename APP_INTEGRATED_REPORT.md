# Relatório: Dashboard Integrado FarmTech Solutions

## Status: Completo e Funcional

**Data:** 21/11/2025  
**Arquivo:** `app_integrated.py`  
**Framework:** Streamlit  
**Linhas de Código:** ~700+

---

## Implementação

### Estrutura Geral

Dashboard unificado com 8 páginas navegáveis via sidebar:

1. Home - Visão geral do projeto
2. Fase 1: Dados & R - Análise estatística CSV
3. Fase 2: Banco de Dados - DER e consultas
4. Fase 3: IoT ESP32 - Visualização do firmware
5. Fase 4: ML Dashboard - Predição de irrigação
6. Fase 5 & Ir Além 1: AWS - Sistema de alertas
7. Fase 6: Visão YOLO - Detecção de pragas
8. Ir Além 2: Algoritmo Genético - Otimização

---

## Detalhamento por Fase

### Home

**Implementado:**
- Card de métricas (6 fases + 2 desafios + 2 modelos IA)
- Descrição do projeto
- Lista de objetivos
- Placeholder para vídeo de apresentação
- Guia de uso

### Fase 1: Dados & R

**Implementado:**
- Carregamento de `fase_1_R_analysis/data/agro_data.csv`
- Exibição de DataFrame com `st.dataframe()`
- Estatísticas descritivas (`describe()`)
- Métricas:
  - Área Total Plantada
  - Produção Total
  - Estados Analisados
  - Produtividade Média

**Gráficos (3 tabs):**
1. Top 10 Estados - Gráfico de barras horizontais
2. Classificação - Gráfico de pizza (Alta/Média/Baixa)
3. Distribuição - Scatter plot (Área vs Produção)

**Tratamento de Erros:**
- Verifica se CSV existe
- Try-except para leitura
- Mensagem amigável se falhar

### Fase 2: Banco de Dados

**Implementado:**
- Exibição da imagem DER
- Fallback inteligente: Busca em múltiplos caminhos
- Descrição do banco: entidades, relacionamentos
- Consulta SQL exemplo (`irrigation_data`)

**Tratamento de Erros:**
- Verifica se imagem existe
- Conecta ao SQLite se disponível
- Mensagens amigáveis

### Fase 3: IoT ESP32

**Implementado:**
- Exibição do código `prog1.ino` com `st.code()`
- Syntax highlighting para C++
- Numeração de linhas
- Lista de componentes (ESP32, DHT22, LDR, etc.)
- Funcionalidades do firmware
- Expander para `diagram.json` (Wokwi)

**Tratamento de Erros:**
- Verifica se .ino existe
- Leitura com encoding UTF-8
- Fallback se diagram.json não existir

### Fase 4: ML Dashboard

**Implementado:**
- Cache de modelo: `@st.cache_resource` para `load_ml_model()`
- Carregamento de `irrigation_model.joblib`
- Interface de predição com sliders:
  - Umidade do Solo (0-100%)
  - pH (0-14)
  - Fósforo (Sim/Não)
  - Potássio (Sim/Não)

**Funcionalidades:**
- Botão "Obter Predição"
- Resultado colorido (verde/azul) baseado na decisão
- Gráfico de Feature Importance
- Seção de explicabilidade

**Tratamento de Erros:**
- Verifica se modelo existe
- Cache para evitar recarregar
- Mensagem de erro amigável

### Fase 5 & Ir Além 1: AWS

**Implementado:**
- Exibição de `aws_comparison_cost.png`
- Integração com `AWSAlertManager` (versão 2.0)
- Persistência no `st.session_state`

**Métricas AWS:**
- Modo de Operação (Simulação/Real)
- Alertas Enviados
- Taxa de Sucesso

**Interface de Testes (3 tipos):**

1. Alerta de Umidade Baixa
   - Inputs: Umidade Atual, Limite Mínimo
   - Chama: `aws_manager.notify_low_humidity()`

2. Detecção de Praga
   - Inputs: Nome da Praga, Confiança (%), Localização
   - Chama: `aws_manager.notify_pest_detection()`

3. Alerta Genérico
   - Inputs: Título, Detalhes, Nível (INFO/WARNING/CRITICAL/EMERGENCY)
   - Chama: `aws_manager.send_alert()`

**Melhorias:**
- Expander para mostrar JSON do resultado
- Mensagens de sucesso/erro claras
- Conversão de % para 0-1 na confiança

Funciona em modo simulação quando AWS não está configurado.

### Fase 6: Visão YOLO

**Implementado:**
- Cache de modelo: `@st.cache_resource` para `load_yolo_model()`
- Carregamento de `best.pt` via `torch.hub.load('ultralytics/yolov5', 'custom')`
- `st.file_uploader()` para imagens (JPG, JPEG, PNG)

**Processamento:**
1. Mostra imagem original (lado esquerdo)
2. Roda detecção com YOLO
3. Mostra imagem com bounding boxes (lado direito)
4. Exibe DataFrame com detecções (`name`, `confidence`)

**Integração AWS Automática:**
- Para cada detecção com confiança > 70%:
  - Exibe warning
  - Botão "Enviar Alerta AWS"
  - Chama `AWSAlertManager.notify_pest_detection()`
  - Mostra resultado em expander

**Tratamento de Erros:**
- Verifica se `best.pt` existe
- Try-except para import torch
- Instruções de instalação se falhar
- Mensagem se nenhum objeto detectado

### Ir Além 2: Algoritmo Genético

**Implementado:**
- Interface completa de configuração:
  - Orçamento Disponível (slider)
  - Número de Culturas (slider)
  - Tamanho da População (slider)
  - Número de Gerações (slider)
  - Taxa de Crossover (slider)
  - Taxa de Mutação (slider)

**Geração de Dados:**
- Botão "Gerar Dados de Culturas"
- Usa `generate_sample_farm_items()`
- Salva no `st.session_state`

**Visualização de Dados:**
- DataFrame com todas as culturas
- Métricas: Custo Total, Valor Total, Razão Valor/Custo

**Botão "Otimizar Recursos":**
1. Cria `FarmGeneticOptimizer`
2. Executa `optimize()` com spinner
3. Mostra resultados:
   - Métricas: Culturas Selecionadas, Valor Total, Custo Total, Utilização (%)
   - Tabela: Culturas escolhidas
   - Gráfico: Evolução do fitness (gerado por `plot_fitness_evolution()`)
   - Insights: Eficiência, performance do algoritmo

**Tratamento de Erros:**
- Try-except no optimize
- Traceback se falhar
- Validações da classe `FarmGeneticOptimizer`

---

## Melhorias Implementadas

### 1. Cache de Modelos (`@st.cache_resource`)

```python
@st.cache_resource
def load_ml_model(model_path):
    """Carrega modelo de ML apenas uma vez"""
    ...

@st.cache_resource
def load_yolo_model(model_path):
    """Carrega modelo YOLO apenas uma vez"""
    ...
```

Modelos carregados uma única vez mesmo com múltiplas interações.

### 2. Persistência de Estado (`st.session_state`)

- `st.session_state.aws_manager` - Reutiliza instância
- `st.session_state.farm_items` - Mantém dados de culturas

Não recria objetos a cada rerun.

### 3. Tratamento de Erros Robusto

Todos os carregamentos incluem:
- Verificação `Path.exists()`
- Try-except com mensagens amigáveis
- Instruções de como resolver

### 4. CSS Customizado

- Classes: `.main-header`, `.phase-header`, `.metric-card`, `.alert-box`
- Cores temáticas (verde agricultura)
- Responsivo

### 5. Navegação Intuitiva

- Sidebar com radio buttons
- Emojis para identificação rápida
- Info box com contato/site

---

## Estatísticas do Código

| Métrica | Valor |
|---------|-------|
| Total de Linhas | ~700+ |
| Fases Implementadas | 6 |
| Desafios "Ir Além" | 2 |
| Gráficos/Visualizações | 7+ |
| Modelos IA Integrados | 2 (ML + YOLO) |
| Funções com Cache | 2 |
| Tipos de Alerta AWS | 3 |
| Tratamento de Erros | 15+ blocos try-except |

---

## Como Testar

### 1. Instalar Dependências

```bash
cd /home/yan/Documents/Git/FarmTech_System
pip install -r requirements.txt
```

### 2. Executar Dashboard

```bash
streamlit run app_integrated.py
```

### 3. Navegação

- Use a barra lateral para alternar entre fases
- Teste os sliders e botões interativos
- Faça upload de imagens na Fase 6
- Configure parâmetros do algoritmo genético

---

## Checklist de Requisitos

| Requisito | Status | Observação |
|-----------|--------|------------|
| Sidebar para navegação | Completo | 8 opções + info box |
| Home com resumo | Completo | Métricas + descrição |
| Fase 1: Carregar CSV | Completo | Com gráficos |
| Fase 2: Exibir DER | Completo | Com fallback |
| Fase 3: Mostrar .ino | Completo | st.code com C++ |
| Fase 4: ML com inputs | Completo | Sliders + predição |
| Fase 5: AWS + Alertas | Completo | AWSAlertManager v2.0 |
| Fase 6: YOLO + upload | Completo | Com auto-alerta |
| Ir Além 2: Genético | Completo | Interface completa |
| `st.cache_resource` | Completo | 2 funções |
| Tratamento de erros | Completo | 15+ blocos |

---

## Suporte

**Arquivo Principal:** `app_integrated.py`

**Dependências:**
- `requirements.txt` (raiz)
- `fase_4_dashboard_ml/scripts/genetic_optimizer.py`
- `fase_4_dashboard_ml/scripts/aws_manager.py`
- `fase_4_dashboard_ml/scripts/utils.py`

**Executar:**
```bash
streamlit run app_integrated.py
```

---

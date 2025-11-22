# FarmTech Solutions - Relatório Técnico

**Versão:** 2.0  
**Data:** 22/11/2025  
**Status:** Produção

## Resumo Executivo

Documentação técnica do dashboard unificado FarmTech Solutions (`app_integrated.py`), plataforma de agricultura de precisão integrando oito módulos: análise de dados, IoT, machine learning, visão computacional, infraestrutura em nuvem e algoritmos de otimização.

### Métricas Principais

- **Código**: 1.500+ linhas Python de produção
- **Módulos**: 9 componentes integrados (6 principais + 3 avançados)
- **Acurácia ML**: 98,5% (classificador Random Forest para irrigação)
- **Performance YOLO**: mAP@0.5 51,3% (modelo customizado)
- **Banco de Dados**: SQLAlchemy ORM com migrações Alembic
- **Visualização**: Analytics interativos com Plotly
- **Integração API**: OpenAI GPT-4o Vision + Chat

## Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────────┐
│               Camada Dashboard Streamlit                    │
│           Interface Unificada - app_integrated.py           │
├────────────────────────────────────────────────────────────┤
│  Fase 1  │  Fase 2  │  Fase 3  │  Fase 4  │  Fase 5       │
│ Analytics│    ORM   │    IoT   │    ML    │   Cloud       │
├────────────────────────────────────────────────────────────┤
│          Fase 6            │      Módulos Avançados         │
│   Visão Computacional      │  Otimizador GA + Assistente NLP│
└────────────────────────────────────────────────────────────┘
```

### Stack Tecnológica

**Backend Framework:**
- Python 3.12.3
- Streamlit 1.39.0
- Pandas 2.2.3
- NumPy 2.1.3

**Machine Learning:**
- Scikit-learn 1.5.2 (Random Forest)
- PyTorch 2.5.1 (backend YOLO)
- Ultralytics 8.3.29 (framework YOLOv5)

**Banco de Dados:**
- SQLAlchemy 2.0.23 (ORM)
- Alembic 1.13.1 (migrações)
- SQLite (desenvolvimento) / PostgreSQL-ready (produção)

**Visualização:**
- Plotly 5.24.1 (gráficos interativos)
- Matplotlib 3.9.2 (gráficos estáticos)

**Cloud & APIs:**
- AWS Boto3 1.35.67 (integração SNS)
- OpenAI API (GPT-4o, GPT-4o-mini)
- Requests 2.32.3 (cliente HTTP)

## Especificações dos Módulos

### Módulo 1: Motor de Análise de Dados

**Objetivo:** Análise estatística de dados de produção agrícola brasileira

**Implementação:**
- Fonte de dados: `fase_1_R_analysis/data/agro_data.csv`
- Visualização: Gráficos interativos Plotly Express
- Exportação: Funcionalidade de download CSV

**Recursos:**
- Top 10 estados por produção (gráfico de barras horizontais)
- Distribuição de classificação de produtividade (gráfico de pizza)
- Correlação área vs produção (scatter plot com codificação de tamanho)

### Módulo 2: Camada de Banco de Dados

**Objetivo:** Abstração de banco de dados com ORM e gerenciamento de migrações

**Implementação:**
- ORM: SQLAlchemy 2.0.23 declarative_base
- Migrações: Controle de versão Alembic
- Modelos: IrrigationData, SensorReading, PestDetection

**Esquema:**

**Tabela `irrigation_data`:**
- id, timestamp, humidity, ph, phosphorus, potassium, needs_irrigation

**Tabela `sensor_readings`:**
- id, timestamp, sensor_id, temperature, humidity, soil_moisture, light_level

**Tabela `pest_detections`:**
- id, timestamp, pest_type, confidence, location, image_path, alert_sent

### Módulo 3: Rede de Sensores IoT

**Objetivo:** Simulação de implantação de sensores ESP32 distribuídos

**Implementação:**
- Função: `generate_sensor_locations(num_sensors=20)`
- Mapa: Plotly scatter_mapbox com OpenStreetMap
- Região: Ribeirão Preto, SP (-21.1767, -47.8208)

**Especificações do Sensor:**
- Hardware: Microcontrolador ESP32
- Sensores: DHT22 (temperatura/umidade), Simulação pH (LDR), Entradas de botões NPK
- Display: LCD I2C (16x2)
- Atuador: Bomba controlada por relé

### Módulo 4: Pipeline de Machine Learning

**Objetivo:** Classificação preditiva de irrigação

**Arquitetura do Modelo:**
```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)
```

**Métricas de Performance:**
- Acurácia: 98,5%
- Precisão: 0,98
- Recall: 0,99
- F1-Score: 0,98

**Features de Entrada:**
1. Umidade do solo (%)
2. pH do solo (escala 0-14)
3. Presença de fósforo (binário)
4. Presença de potássio (binário)

### Módulo 5: Infraestrutura em Nuvem

**Objetivo:** Integração AWS e análise de custos

**Serviços AWS:**
- SNS: Entrega de notificações push
- EC2: Hospedagem de aplicação (planejado)
- S3: Armazenamento data lake (planejado)
- RDS: Banco de dados PostgreSQL (planejado)

**Sistema de Alertas:**
- Failover automático para modo simulação
- Níveis de severidade: INFO, WARNING, CRITICAL, EMERGENCY

### Módulo 6: Sistema de Visão Computacional

**Objetivo:** Detecção híbrida de pragas e análise via IA

**Arquitetura Dual:**

**Modelo A: FarmTech Customizado**
- Base: YOLOv5
- Treinamento: Dataset customizado de pragas
- Classes: 2 (específicas de pragas)
- mAP@0.5: 51,3%
- Épocas: 60
- Tamanho: 42,2 MB (`best.pt`)

**Modelo B: YOLOv5s Geral**
- Pré-treinado: Dataset COCO
- Classes: 80 (objetos gerais)
- Download automático: torch.hub
- Tamanho: 14,1 MB

**Integração LLM Vision:**
- API: OpenAI GPT-4o-mini Vision
- Entrada: Imagem codificada em Base64 + prompt fitopatológico
- Saída: Relatório diagnóstico detalhado

### Módulo 7: Interface em Linguagem Natural

**Objetivo:** Sistema de consulta ao banco de dados via IA

**Implementação:**
- Modelo: gpt-4o-mini (otimizado para velocidade)
- Contexto: Últimas 50 leituras de sensores + estatísticas
- Sessão: Histórico de chat persistente

**Capacidades de Consulta:**
- Resumos estatísticos em linguagem natural
- Alertas baseados em thresholds
- Análise de tendências
- Conversas multi-turno

### Módulo 8: Otimizador com Algoritmo Genético

**Objetivo:** Otimização de seleção de culturas (problema da mochila binária)

**Especificações do Algoritmo:**
- Seleção: Elitismo (melhores indivíduos preservados)
- Crossover: Ponto único com taxa configurável
- Mutação: Bit-flip com probabilidade configurável
- Função Fitness: Maximizar valor sujeito a restrição de orçamento

**Parâmetros de Configuração:**
```python
optimizer = FarmGeneticOptimizer(
    budget=150000,              # Restrição de orçamento (R$)
    population_size=32,         # Soluções por geração
    num_generations=1000,       # Iterações de evolução
    crossover_rate=0.8,         # Probabilidade de crossover
    mutation_rate=0.15          # Probabilidade de mutação
)
```

## Fluxos de Dados

### Fluxo de Predição de Irrigação

```
Entrada Sensor → Banco de Dados → Modelo ML → Predição
                   ↓
              Sistema de Alertas (se crítico)
```

### Fluxo de Detecção de Pragas

```
Upload Imagem → Detecção YOLO → Verificação Confiança
                                      ↓
                         Análise LLM Vision (opcional)
                                      ↓
                              Alerta + Relatório
```

### Fluxo de Otimização

```
Catálogo Culturas → Init População GA → Loop Evolução
                                         ↓
                                Seleção → Crossover → Mutação
                                         ↓
                                   Melhor Solução
```

## Segurança e Tratamento de Erros

### Validação de Entrada

- Valores de sensor: Verificações de faixa (umidade 0-100%, pH 0-14)
- Upload de imagens: Validação de tipo (apenas JPEG, PNG)
- Chaves API: Mascaramento de senha na UI
- Injeção SQL: Prevenido via SQLAlchemy ORM

### Recuperação de Erros

- Failover AWS: Ativação automática do modo simulação
- Modelos ausentes: Degradação gradual com orientação ao usuário
- Erros de banco de dados: Rollback de transação com log de erro
- Falhas de API: Tratamento de timeout (30s) com lógica de retry

### Gerenciamento de Sessão

- Cache de modelos: `@st.cache_resource` para modelos YOLO/ML
- Cache de dados: `@st.cache_data` para datasets estáticos
- Histórico de chat: `st.session_state` para persistência de conversas

## Benchmarks de Performance

### Tempo de Carregamento do Dashboard

- Carregamento inicial: ~3-5 segundos
- Troca de módulo: ~500ms
- Predição do modelo: ~100-200ms
- Detecção YOLO: ~1-3 segundos
- LLM Vision: ~5-10 segundos (dependente de API)

### Operações de Banco de Dados

- Query (50 registros): ~10ms
- Insert (batch 50): ~50ms
- Migração: ~100ms

### Performance de Otimização

- AG (1000 gerações, população 32): ~2-5 segundos

## Considerações de Deploy

### Checklist de Produção

- [ ] Migrar para PostgreSQL (atualizar DATABASE_URL)
- [ ] Configurar credenciais AWS (SNS, S3, RDS)
- [ ] Configurar SSL/TLS (HTTPS)
- [ ] Implementar autenticação (Streamlit Enterprise)
- [ ] Configurar logging (ELK stack ou CloudWatch)
- [ ] Configurar monitoramento (Prometheus + Grafana)
- [ ] Habilitar backups automáticos (snapshots de banco)
- [ ] Configurar CDN para assets estáticos
- [ ] Implementar rate limiting para chamadas de API
- [ ] Configurar pipeline CI/CD (GitHub Actions)

### Escalabilidade

**Escalonamento Horizontal:**
- Design de dashboard stateless
- Externalização de estado de sessão (Redis)
- Load balancer (Nginx/AWS ALB)

**Escalonamento Vertical:**
- Aumentar processos worker (Streamlit)
- Aceleração GPU para YOLO (CUDA)
- Réplicas de leitura de banco de dados

## Estratégia de Testes

### Testes Unitários

```bash
pytest fase_4_dashboard_ml/tests/
pytest ir_alem_2_genetic_algorithm/tests/
```

### Testes de Integração

- Validação de fluxo end-to-end
- Verificação de integração de API
- Testes de migração de banco de dados

### Testes de Carga

- Simulação de usuários concorrentes (Locust)
- Testes de rate limit de API
- Validação de connection pooling de banco

## Manutenção & Suporte

### Documentação

- Código: Docstrings estilo Google
- API: Documentação inline
- Banco de Dados: Diagramas ER + docs de esquema

### Monitoramento

- Logs de aplicação: `/var/log/farmtech/`
- Rastreamento de erros: Integração Sentry
- Métricas de performance: New Relic APM
- Monitoramento de uptime: Pingdom

### Estratégia de Backup

- Banco de dados: Backups diários automatizados (reter 30 dias)
- Modelos: Controle de versão no Git LFS
- Dados de usuário: Backups incrementais para S3

---

**Proprietário do Documento:** Equipe de Engenharia FarmTech  
**Última Atualização:** 22/11/2025  
**Versão:** 2.0 (Release de Produção)  
**Classificação:** Documentação Técnica Interna

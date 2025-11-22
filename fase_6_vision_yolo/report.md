# Relatório de Projeto Completo: Visão Computacional FarmTech Solutions

**🎥 [Vídeo Demonstrativo](https://youtu.be/LlLFZXPC-bU)**

**Projeto:** Solução Completa de Visão Computacional - Detecção e Classificação de Objetos
**Equipe FarmTech Vision Lab:**
- Yan Pimentel Cotta - RM: 562836
- Jonas T V Fernandes - RM: 563027
- Raphael da Silva - RM: 561452
- Raphael Dinelli Neto - RM: 562892
- Levi Passos Silveira Marques - RM: 565557

**Período de Desenvolvimento:** Outubro de 2025
**Tecnologias:** Python, YOLOv5, PyTorch, TensorFlow/Keras, MobileNetV2, Google Colab, Google Drive, Make Sense AI

**Documentação relacionada:** 
- Visão geral: [README](../README.md)
- Orientações oficiais: [orientation.md](orientation.md)
- Notebooks executáveis: 
  - [`entregavel_1_fase6_cap1.ipynb`](../notebooks/entregavel_1_fase6_cap1.ipynb) (Entrega 1)
  - [`Entrega2_RaphaelDaSilva_RM561452_fase6_cap1.ipynb`](../notebooks/Entrega2_RaphaelDaSilva_RM561452_fase6_cap1.ipynb) (Entrega 2)
  - [`ir_alem_opcao_2_fase_6_cap1.ipynb`](../notebooks/ir_alem_opcao_2_fase_6_cap1.ipynb) (Ir Além 2)

---

## **1.0 Resumo Executivo**

Este relatório documenta o desenvolvimento de uma solução completa de visão computacional para a FarmTech Solutions, apresentando três entregas complementares que exploram diferentes aspectos de detecção e classificação de objetos utilizando Deep Learning. O projeto foi desenvolvido ao longo da Fase 6 do curso de IA/ML da FIAP, seguindo rigorosamente as orientações estabelecidas no documento [`orientation.md`](orientation.md).

### Visão Geral das Entregas

**Entrega 1 - Detecção Customizada com YOLOv5:**
A primeira entrega estabeleceu a base do projeto com uma Prova de Conceito (PoC) completa de detecção de objetos. Foram conduzidos três experimentos controlados — dois com a arquitetura **YOLOv5s** (30 e 60 épocas) e um com a arquitetura **YOLOv5m** (60 épocas) — para detectar objetos das classes `banana` e `fork`. O modelo campeão (`YOLOv5m`) alcançou **mAP@.50 geral de 0.789**, com desempenho praticamente perfeito na classe `banana` (0.995) e avanço significativo na classe `fork` (0.584).

**Entrega 2 - Comparação YOLO vs CNN:**
A segunda entrega expandiu a análise através de um estudo comparativo entre a arquitetura YOLOv5 (focada em detecção) e uma Rede Neural Convolucional customizada (focada em classificação). A CNN foi desenvolvida do zero e treinada em dois cenários (30 e 60 épocas), permitindo uma avaliação criteriosa dos trade-offs entre facilidade de uso, precisão, tempo de treinamento e aplicabilidade de cada abordagem.

**Ir Além 2 - Pipeline Integrado com Transfer Learning:**
A entrega adicional demonstrou técnicas avançadas através de um pipeline de duas etapas que combina YOLOv5 para detecção de ROI (Região de Interesse) com MobileNetV2 para classificação via transfer learning. Esta abordagem híbrida resultou em melhorias significativas de acurácia (+12.50 pontos) e precisão (+17.86 pontos) em comparação com classificação direta.

### Principais Conquistas
- Dataset proprietário de 80 imagens com alta variabilidade de condições
- Pipeline completo de MLOps desde coleta até deploy
- Análise quantitativa e qualitativa detalhada de múltiplas arquiteturas
- Documentação executiva alinhada às melhores práticas de governança
- Recomendações estratégicas para diferentes cenários de implantação

---

## **2.0 Metodologia e Plano de Ação**

O projeto seguiu rigorosamente as orientações estabelecidas no documento [`orientation.md`](orientation.md), que define os requisitos, metas e entregáveis para a Fase 6 do curso. A metodologia adotada segue as melhores práticas de desenvolvimento de modelos de Machine Learning, com ênfase em reprodutibilidade, documentação e governança.

### 2.1 Alinhamento com Requisitos da Fase 6

Conforme especificado nas orientações, o projeto atende aos seguintes requisitos:

**Metas da Entrega 1 (Atendidas):**
- ✅ Dataset com mínimo de 40 imagens por classe (A e B), totalizando 80 imagens
- ✅ Divisão estratificada: 32 imagens/classe para treino, 4 para validação, 4 para teste
- ✅ Armazenamento no Google Drive com separação adequada
- ✅ Rotulação no Make Sense AI com exportação para formato YOLO
- ✅ Notebook no Google Colab com documentação Markdown completa
- ✅ Múltiplas simulações com diferentes épocas (30 e 60) comparando acurácia e desempenho
- ✅ Apresentação de conclusões sobre validação e testes
- ✅ Prints das imagens processadas demonstrando resultados

**Entregáveis da Entrega 1 (Cumpridos):**
- ✅ Repositório GitHub público com nome do grupo (FarmTech Vision Lab)
- ✅ Notebook com código executado e células Markdown organizadas
- ✅ Vídeo demonstrativo de até 5 minutos no YouTube (não listado)
- ✅ README com documentação introdutória integrada ao notebook
- ✅ Repositório mantido público para acesso da equipe FIAP

### 2.2 Fases de Execução do Projeto

**Fase 0: Setup e Fundação do Ambiente**
- Configuração do versionamento de código (Git/GitHub)
- Estruturação de armazenamento de dados (Google Drive com hierarquia `/datasets/images/` e `/datasets/labels/`)
- Configuração do ambiente de desenvolvimento (Google Colab com GPU T4)

**Fase 1: Aquisição e Preparação dos Dados**
- Seleção estratégica dos objetos (`banana` e `fork`) baseada em distinção visual e disponibilidade
- Coleta de dataset proprietário com 80 imagens (40 por classe)
- Captura com variabilidade controlada de ângulos, iluminação e fundos
- Divisão estratificada: 64 treino (80%), 8 validação (10%), 8 teste (10%)

**Fase 2: Anotação dos Dados**
- Rotulação manual no Make Sense AI usando bounding boxes retangulares
- Exportação para formato YOLO (arquivos .txt com coordenadas normalizadas)
- Validação de integridade das anotações
- Armazenamento sincronizado com Google Drive

**Fase 3: Desenvolvimento e Treinamento**
- **Entrega 1**: Três experimentos controlados com YOLOv5
  - YOLOv5s com 30 épocas (baseline)
  - YOLOv5s com 60 épocas (avaliar impacto de épocas adicionais)
  - YOLOv5m com 60 épocas (avaliar impacto de arquitetura maior)
- **Entrega 2**: Comparação com CNN customizada
  - Desenvolvimento de arquitetura sequencial do zero
  - Treinamento com 30 e 60 épocas
- **Ir Além 2**: Pipeline integrado avançado
  - Transfer learning com MobileNetV2
  - Pré-processamento inteligente com YOLOv5

**Fase 4: Análise e Avaliação**
- Análise quantitativa: métricas de mAP@.50, precisão, recall, F1-score
- Análise qualitativa: inspeção visual das predições
- Comparação de trade-offs: acurácia vs custo computacional vs tamanho do modelo
- Documentação detalhada de limitações e desafios encontrados

**Fase 5: Inferência e Validação Final**
- Teste em conjunto de imagens nunca vistas durante treinamento
- Validação da capacidade de generalização
- Geração de visualizações e relatórios de resultados

**Fase 6: Empacotamento e Entrega**
- Finalização da documentação executiva (README.md e report.md)
- Produção de vídeos demonstrativos
- Geração de gráficos comparativos e tabelas executivas
- Submissão via portal FIAP

---

## **3.0 Execução Detalhada do Projeto (Changelog)**

### 3.1 Entrega 1: Detecção Customizada com YOLOv5

**Setup do Ambiente:**
- Inicializado repositório GitHub (YOLO_vision_demo) com template `.gitignore` para Python
- Estruturada hierarquia de pastas no Google Drive: `/datasets/images/` e `/datasets/labels/`
- Configurado Google Colab com GPU T4 para treinamento acelerado
- Clonado repositório oficial do YOLOv5 da Ultralytics

**Aquisição de Dados:**
- Selecionadas classes `banana` e `fork` por distinção visual e disponibilidade física
- Coletadas 80 imagens proprietárias (40 por classe) com variabilidade de:
  - Ângulos de captura (frontal, lateral, diagonal)
  - Condições de iluminação (natural, artificial, mista)
  - Fundos diversos (uniforme, texturizado, complexo)
- Divisão estratificada 80/10/10: 64 treino, 8 validação, 8 teste

**Anotação de Dados:**
- Rotulagem no Make Sense AI com bounding boxes retangulares
- Exportação para formato YOLO (arquivos .txt com coordenadas normalizadas)
- Primeira tentativa usou polígonos (incompatível) - re-anotação necessária
- 72 imagens anotadas (treino + validação)

**Treinamento e Experimentação:**
- **Experimento 1 - YOLOv5s 30 épocas**:
  - Peso inicial: `yolov5s.pt` (pré-treinado em COCO)
  - Tempo de treino: 0.56h (CPU, primeiro experimento)
  - mAP@.50 geral: 0.393
  - mAP@.50 banana: 0.687 | fork: 0.0999
  - Tamanho do modelo: 14.4 MB
  
- **Experimento 2 - YOLOv5s 60 épocas**:
  - Peso inicial: `yolov5s.pt`
  - Tempo de treino: 1.13h (CPU)
  - mAP@.50 geral: 0.513 (+30.5% vs Exp1)
  - mAP@.50 banana: 0.764 | fork: 0.262
  - Tamanho do modelo: 14.4 MB
  
- **Experimento 3 - YOLOv5m 60 épocas** (Modelo Campeão):
  - Peso inicial: `yolov5m.pt`
  - Tempo de treino: 0.13h (GPU T4)
  - mAP@.50 geral: 0.789 (+53.8% vs melhor YOLOv5s)
  - mAP@.50 banana: 0.995 | fork: 0.584
  - Tamanho do modelo: 42.2 MB

**Inferência e Validação:**
- Testes realizados no conjunto separado (8 imagens)
- Análise qualitativa com visualizações de bounding boxes
- Geração de gráficos comparativos de métricas
- Exportação de artefatos para Google Drive

**Produtos Gerados:**
- Notebook completo com células Markdown narrativas
- Vídeo demonstrativo de 5 minutos no YouTube
- Gráficos: curvas de aprendizado, comparativo de barras, curvas de perda
- Tabela comparativa executiva dos três experimentos

### 3.2 Entrega 2: Comparação YOLO vs CNN

**Desenvolvimento da CNN:**
- Arquitetura sequencial customizada desenvolvida no Keras:
  - Camadas Conv2D com 32 e 64 filtros (kernel 3×3, ReLU)
  - MaxPooling 2×2 para redução de dimensionalidade
  - Flatten + Dense (128 neurônios, ReLU)
  - Dropout (0.5) para regularização
  - Camada de saída Dense (2 neurônios, Softmax)
- Compilação: otimizador Adam, loss categorical crossentropy
- Imagens redimensionadas para 150×150 pixels

**Treinamento da CNN:**
- **CNN 30 épocas**:
  - Acurácia treino: ~97%
  - Acurácia validação: ~84%
  - Observadas oscilações entre épocas
  
- **CNN 60 épocas**:
  - Acurácia treino: ~97%
  - Acurácia validação: ~95.9%
  - Melhor estabilidade e generalização

**Análise Comparativa:**
Comparação sistemática entre YOLO e CNN considerando:
- **Facilidade de uso**: YOLO com ferramentas prontas vs CNN que requer implementação manual
- **Precisão**: YOLO superior para detecção multi-objeto, CNN adequada para classificação
- **Tempo de treinamento**: CNN mais rápida devido à simplicidade arquitetural
- **Tempo de inferência**: YOLO otimizada para tempo real, CNN eficiente para classificação pura

**Conclusões da Entrega 2:**
- YOLOv5 demonstrou superioridade para detecção de objetos em tempo real
- CNN mais adequada para tarefas de classificação onde localização não é necessária
- Trade-offs claros entre complexidade de implementação e versatilidade

### 3.3 Ir Além 2: Pipeline Integrado com Transfer Learning

**Abordagem 1 - Baseline (MobileNetV2 puro):**
- Modelo pré-treinado no ImageNet
- Fine-tuning das camadas superiores
- Treinamento em dataset completo sem pré-processamento
- Resultados baseline:
  - Acurácia: 75%
  - Precisão: 67.86%
  - Recall: 100%

**Abordagem 2 - Pipeline Integrado:**
- **Etapa 1**: YOLOv5 para detecção e recorte de ROI
  - Uso do modelo treinado na Entrega 1
  - Identificação automática de objetos nas imagens
  - Recorte inteligente da região de interesse
- **Etapa 2**: MobileNetV2 para classificação
  - Classificação sobre ROIs extraídas
  - Redução de ruído de fundo
  - Foco na região relevante do objeto

**Resultados do Pipeline Integrado:**
- Acurácia: 87.50% (+12.50 pontos vs baseline)
- Precisão: 85.71% (+17.86 pontos vs baseline)
- Recall: 75% (-25 pontos vs baseline)

**Análise de Trade-offs:**
- Ganho significativo em precisão (menos falsos positivos)
- Redução em recall indica falhas na detecção inicial (YOLOv5)
- Pipeline mais complexo mas com melhor confiabilidade
- Adequado para aplicações onde precisão é crítica

**Recomendações:**
- Pipeline integrado para contextos que exigem alta confiabilidade
- Baseline direto para máxima cobertura (recall)
- Possibilidade de ajuste de thresholds conforme necessidade do negócio

---

## **4.0 Desafios Encontrados e Soluções Aplicadas**

### 4.1 Desafios da Entrega 1

**Desafio 1: Incompatibilidade de Anotação (Polígonos vs. Bounding Boxes)**
- **Problema:** Primeira tentativa de anotação utilizou polígonos para maximizar precisão. O Make Sense AI não suporta exportação de polígonos para formato YOLO, que requer estritamente bounding boxes retangulares.
- **Solução:** Re-anotação completa do dataset (72 imagens) utilizando ferramenta de bounding box.
- **Aprendizado:** Crítico alinhar metodologia de anotação com requisitos de entrada do modelo antes de iniciar trabalho manual. Esta experiência reforçou importância de validar compatibilidade de ferramentas no início do pipeline.
- **Impacto:** Atraso de aproximadamente 4 horas no cronograma, mas garantiu compatibilidade total com YOLOv5.

**Desafio 2: Perda de Contexto de Diretório no Colab**
- **Problema:** Após interrupção de célula de treinamento, ambiente Colab perdeu contexto do diretório de trabalho (`/content/yolov5/`), causando `FileNotFoundError` ao reexecutar `train.py`.
- **Solução:** Adição de comando `%cd /content/yolov5/` no início de todas as células de execução de scripts, garantindo diretório correto independente do estado da sessão.
- **Aprendizado:** Importância de tornar notebooks robustos contra interrupções, especialmente em ambientes de nuvem com timeouts.

**Desafio 3: Formato de Imagem Inválido (.AVIF)**
- **Problema:** Durante treinamento, YOLOv5 emitiu avisos sobre duas imagens `.AVIF` que não puderam ser lidas e foram ignoradas.
- **Solução:** Identificação e conversão das imagens para formatos padrão (`.jpg` ou `.png`). Treinamento prosseguiu com dataset reduzido, mas correção implementada para futuras iterações.
- **Aprendizado:** Necessidade de validação de formatos de imagem antes do treinamento. Implementação de script de verificação automática recomendada para futuros projetos.

**Desafio 4: Limitações de Bounding Boxes para Geometrias Irregulares**
- **Problema:** Objetos com geometria irregular (garfos angulados, bananas curvas) sofrem com representação em bounding boxes retangulares, que capturam excesso de fundo e reduzem razão sinal-ruído.
- **Impacto:** Classe `fork` apresentou desempenho inferior (mAP@.50 de 0.584 no melhor modelo vs 0.995 para `banana`).
- **Mitigação Parcial:** Arquitetura YOLOv5m mais robusta melhorou significativamente detecção de `fork` (0.0999 → 0.584).
- **Roadmap Futuro:** Considerar segmentação de instâncias (Mask R-CNN, YOLACT) para objetos irregulares.

### 4.2 Desafios da Entrega 2

**Desafio 5: Comparação entre Tarefas Diferentes (Detecção vs Classificação)**
- **Problema:** YOLO realiza detecção de objetos (localização + classificação) enquanto CNN faz apenas classificação. Comparação direta de métricas pode ser enganosa.
- **Solução:** Análise focada em diferentes aspectos: YOLO avaliado por mAP, precision, recall para detecção; CNN avaliada por acurácia de classificação. Comparação contextualizada no domínio de aplicação.
- **Aprendizado:** Importância de definir métricas apropriadas para cada arquitetura e contexto de uso.

**Desafio 6: Overfitting em CNN Simples**
- **Problema:** CNN com arquitetura simples apresentou sinais de overfitting com alta acurácia de treino (97%) mas acurácia de validação variável.
- **Solução:** Adição de camada Dropout (0.5) e aumento do número de épocas para 60, melhorando estabilidade.
- **Resultado:** Acurácia de validação estabilizou em ~95.9%.

### 4.3 Desafios do Ir Além 2

**Desafio 7: Trade-off Precision vs Recall no Pipeline Integrado**
- **Problema:** Pipeline YOLOv5 + MobileNetV2 mostrou excelente precisão (85.71%) mas recall reduzido (75% vs 100% no baseline).
- **Causa Raiz:** Falhas na detecção inicial pelo YOLOv5 resultam em perda de objetos antes da classificação.
- **Análise:** Este não é uma falha, mas um insight valioso sobre dinâmica entre confiabilidade e abrangência.
- **Recomendação:** Para contextos críticos onde falsos positivos são custosos, usar pipeline integrado. Para máxima cobertura, usar baseline direto.

**Desafio 8: Complexidade Computacional do Pipeline**
- **Problema:** Pipeline de duas etapas requer mais recursos e tempo de inferência que classificação direta.
- **Impacto:** Tempo de inferência aproximadamente 2x maior.
- **Justificativa:** Ganho de +17.86 pontos em precisão justifica overhead para aplicações que exigem alta confiabilidade.
- **Otimização Futura:** Considerar batch processing e otimizações de modelo (quantização, pruning).

---

## **5.0 Análise de Resultados**

### 5.1 Resultados da Entrega 1: Detecção YOLOv5

**Comparativo de Desempenho dos Três Experimentos:**

| Métrica               | YOLOv5s 30 Épocas | YOLOv5s 60 Épocas | YOLOv5m 60 Épocas | Análise |
| --------------------- | -----------------: | -----------------: | -----------------: | ------- |
| **mAP@.50 (Geral)**   | 0.393 | 0.513 | **0.789** | Modelo médio superior em 53.8% |
| mAP@.50 (banana)      | 0.687 | 0.764 | **0.995** | Praticamente saturado |
| mAP@.50 (fork)        | 0.0999 | 0.262 | **0.584** | Melhora dramática: 484% |
| Tamanho modelo (MB)   | 14.4 | 14.4 | 42.2 | Trade-off: +193% tamanho |
| Tempo treino (h)      | 0.56 | 1.13 | 0.13 | GPU T4 muito mais eficiente |

**Principais Insights:**

1. **Impacto do Tempo de Treinamento:** Salto de 30 para 60 épocas no `YOLOv5s` elevou mAP@.50 geral de 0.393 para 0.513 (+30,5%), eliminando sinais de underfitting observados no experimento inicial. A classe `fork` beneficiou-se especialmente, saltando de 0.0999 para 0.262 (+162%).

2. **Impacto da Complexidade Arquitetural:** Migração para `YOLOv5m` elevou mAP@.50 geral para 0.789 (+53,8% sobre melhor modelo pequeno). Desempenho em `fork` mais que dobrou (0.262 → 0.584), demonstrando que arquitetura mais robusta captura melhor nuances de objetos irregulares.

3. **Trade-off de Tamanho:** YOLOv5m apresenta aumento de ~200% no tamanho (14 MB → 42 MB). Este custo deve ser considerado em:
   - Restrições de armazenamento em dispositivos edge
   - Tempo de carregamento do modelo
   - Estratégias de versionamento em MLOps
   - Largura de banda para deploy remoto

4. **Eficiência de Hardware:** GPU T4 demonstrou throughput muito superior (0.13h vs 1.13h para 60 épocas), validando importância de hardware adequado para experimentação ágil.

**Análise Qualitativa:**
- Classe `banana`: Detecção praticamente perfeita em todas as condições testadas
- Classe `fork`: Melhora significativa com YOLOv5m, mas ainda apresenta desafios em:
  - Ângulos muito oblíquos
  - Fundos com texturas metálicas similares
  - Oclusões parciais
- Limitação de bounding boxes: Objetos irregulares capturam muito ruído de fundo, sugerindo segmentação como evolução futura

### 5.2 Resultados da Entrega 2: YOLO vs CNN

**Comparativo Qualitativo:**

| Critério | YOLO Tradicional | CNN Customizada |
| -------- | ---------------- | --------------- |
| **Facilidade de uso** | Alta - ferramentas prontas, integração simplificada | Média - requer implementação manual |
| **Precisão** | Alta para detecção multi-objeto com localização | Alta para classificação pura |
| **Tempo treinamento** | Moderado (60 épocas: ~1h CPU, 0.13h GPU) | Rápido (60 épocas: menor devido à simplicidade) |
| **Tempo inferência** | Otimizado para tempo real (~10-30ms por imagem) | Eficiente para classificação única |
| **Aplicabilidade** | Detecção, localização, contagem de objetos | Classificação binária/multi-classe |

**Conclusões da Comparação:**
- **YOLOv5 superior quando**: Necessário localizar objetos, detectar múltiplos objetos simultaneamente, aplicações em tempo real
- **CNN adequada quando**: Apenas classificação necessária, imagens pré-recortadas, recursos computacionais limitados para inferência simples
- **Trade-offs fundamentais**: Complexidade vs versatilidade, implementação vs performance

### 5.3 Resultados do Ir Além 2: Pipeline Integrado

**Comparativo Quantitativo:**

| Métrica | Baseline (MobileNetV2) | Pipeline Integrado (YOLO + MobileNetV2) | Delta |
| ------- | ---------------------: | ---------------------------------------: | ----: |
| **Acurácia** | 75.00% | **87.50%** | +12.50 |
| **Precisão** | 67.86% | **85.71%** | +17.86 |
| **Recall** | 100.00% | 75.00% | -25.00 |
| **F1-Score** | 80.95% | 80.00% | -0.95 |

**Análise de Trade-offs:**

1. **Ganho em Precisão (+17.86 pontos):**
   - Pipeline elimina muito ruído de fundo através do recorte inteligente
   - Classificador foca apenas na região relevante
   - Redução drástica de falsos positivos
   - **Ideal para**: Aplicações onde custo de falso positivo é alto (ex: sistemas de segurança, controle de qualidade)

2. **Perda em Recall (-25 pontos):**
   - Falhas na detecção YOLOv5 resultam em objetos não classificados
   - Pipeline cascata amplifica erros da primeira etapa
   - **Mitigação**: Ajustar threshold de confiança do YOLOv5 para máxima sensibilidade
   - **Trade-off consciente**: Aceitar mais falsos positivos no detector para maximizar recall final

3. **Estabilidade de F1-Score:**
   - F1-Score praticamente idêntico (80.95% vs 80.00%) indica rebalanceamento de erros
   - Mudança de perfil: menos falsos positivos, mais falsos negativos
   - Escolha de pipeline deve ser guiada por contexto de negócio

**Recomendações por Contexto:**

| Contexto | Pipeline Recomendado | Justificativa |
| -------- | ------------------- | ------------- |
| Controle de qualidade industrial | Pipeline Integrado | Alta precisão crítica; falsos positivos custosos |
| Triagem médica inicial | Baseline | Recall 100% essencial; falsos positivos revisados por humanos |
| Sistema de segurança | Pipeline Integrado | Confiabilidade de alertas prioritária |
| Monitoramento ambiental | Baseline | Máxima cobertura para não perder eventos raros |

### 5.4 Análise Consolidada das Três Entregas

**Progressão de Conhecimento:**
1. **Entrega 1**: Estabeleceu fundação sólida em detecção, compreensão de trade-offs arquiteturais
2. **Entrega 2**: Expandiu compreensão comparando paradigmas diferentes (detecção vs classificação)
3. **Ir Além 2**: Demonstrou técnicas avançadas de integração e otimização de pipelines

**Lições Aprendidas:**
- Não existe modelo "melhor" universal - apenas modelo mais adequado para contexto específico
- Trade-offs entre métricas refletem decisões de engenharia, não falhas
- Documentação detalhada e análise quantitativa são essenciais para decisões informadas
- Pipelines complexos oferecem oportunidades de otimização mas introduzem pontos de falha adicionais

---

## **6.0 Recomendações Estratégicas**

### 6.1 Recomendações por Cenário de Deploy

**Cenário 1: Ambientes com Recursos Amplos (Cloud/Desktop)**
- **Modelo Recomendado**: YOLOv5m (60 épocas)
- **Justificativa**: mAP@.50 de 0.789, excelente equilíbrio entre acurácia e tempo de inferência
- **Tamanho**: 42.2 MB facilmente gerenciável em infraestrutura cloud
- **Aplicações**: Sistemas de monitoramento centralizados, processamento em lote, análise retrospectiva
- **Melhorias Sugeridas**: 
  - Considerar YOLOv5l ou YOLOv5x para incremento adicional de acurácia
  - Implementar ensemble de modelos para máxima confiabilidade

**Cenário 2: Dispositivos Embarcados (Edge com Restrições)**
- **Modelo Recomendado**: YOLOv5s com otimizações
- **Justificativa**: 14.4 MB mais adequado para dispositivos com memória limitada
- **Estratégias de Otimização**:
  - **Quantização**: Converter de FP32 para INT8 (redução de ~75% em tamanho)
  - **Pruning**: Remover pesos menos importantes (redução adicional de 30-50%)
  - **Knowledge Distillation**: Treinar modelo menor com supervisão do YOLOv5m
- **Trade-off Esperado**: Manter 80-90% da acurácia do modelo grande
- **Aplicações**: ESP32-CAM, Raspberry Pi, sistemas IoT, câmeras inteligentes

**Cenário 3: Aplicações Críticas (Alta Precisão)**
- **Pipeline Recomendado**: YOLOv5m + MobileNetV2 (Ir Além 2)
- **Justificativa**: Precisão de 85.71% minimiza falsos positivos
- **Aplicações**: Controle de qualidade, sistemas de segurança, aplicações médicas
- **Considerações**: Aceitar recall reduzido (75%) e maior latência
- **Otimização**: Ajustar threshold de confiança do YOLOv5 conforme tolerância a falsos positivos

**Cenário 4: Máxima Cobertura (Alto Recall)**
- **Pipeline Recomendado**: Baseline direto (MobileNetV2) ou YOLO com threshold baixo
- **Justificativa**: Recall de 100% garante nenhum objeto perdido
- **Aplicações**: Triagem inicial, monitoramento ambiental, sistemas de alerta
- **Pós-processamento**: Revisão humana de falsos positivos aceitável

### 6.2 Roadmap de Evolução Técnica

**Curto Prazo (1-3 meses):**

1. **Expansão de Dataset**
   - Alvo: 200+ imagens por classe
   - Foco: Cenários adversos (baixa iluminação, oclusão, múltiplos objetos)
   - Diversificação: Novos objetos, diferentes categorias
   
2. **Data Augmentation Avançado**
   - Técnicas: Cutout, Copy-Paste, Mixup, CutMix
   - Ajustes: Cores (HSV), rotação, scale, flip
   - Objetivo: Simular variabilidade real sem coleta adicional
   
3. **Avaliação Automática**
   - Implementar pipeline de CI/CD para modelos
   - Alertas quando mAP@.50 < 0.70
   - Dashboards de monitoramento contínuo

**Médio Prazo (3-6 meses):**

1. **Otimização de Hiperparâmetros**
   - Framework: Optuna ou Ray Tune
   - Parâmetros: Learning rate, momentum, weight decay, augmentation intensity
   - Objetivo: Ganho de 5-10% em mAP@.50
   
2. **Segmentação de Instâncias**
   - Modelos: Mask R-CNN, YOLACT, YOLOv8-Seg
   - Objetivo: Superar limitação de bounding boxes
   - Métrica alvo: IoU (Intersection over Union) > 0.80
   
3. **Compressão de Modelos**
   - Pipeline: Pruning estruturado + Quantização INT8 + ONNX Runtime
   - Objetivo: YOLOv5m com tamanho de YOLOv5s (~15 MB)
   - Restrição: Manter mAP@.50 > 0.70

**Longo Prazo (6-12 meses):**

1. **MLOps e Governança**
   - Versionamento de dados: DVC (Data Version Control)
   - Tracking de experimentos: MLflow, Weights & Biases
   - CI/CD para modelos: GitHub Actions + Model Registry
   - Monitoramento pós-deploy: Drift detection, performance degradation alerts
   
2. **Integração com Sistemas FarmTech**
   - APIs REST/gRPC para inferência
   - Dashboards executivos com métricas de negócio
   - Integração com sistemas legados (ERP, CRM)
   - Feedback loop: Predições → Validação → Retreinamento
   
3. **Expansão de Capacidades**
   - Detecção de múltiplas classes (10+ objetos)
   - Rastreamento de objetos (tracking) em vídeo
   - Análise temporal: Contagem, comportamento, padrões
   - Modelos especializados por contexto (indoor vs outdoor, dia vs noite)

### 6.3 Governança de Dados e Compliance

**Qualidade de Dados:**
- **Checklist de Validação**:
  ✓ Formatos de imagem padronizados (JPEG/PNG)
  ✓ Resolução mínima (640x640 pixels)
  ✓ Anotações validadas por segundo revisor
  ✓ Metadados completos (timestamp, condições de captura)
  
- **Auditoria de Rotulagem**:
  - Revisão periódica de 10% das anotações
  - Inter-annotator agreement (Cohen's Kappa > 0.80)
  - Re-anotação de casos ambíguos

**Reprodutibilidade:**
- **Registro de Experimentos**:
  - Parâmetros de treinamento (épocas, learning rate, batch size)
  - Hardware utilizado (CPU/GPU, memória)
  - Seed aleatório para reprodução exata
  - Timestamp e identificador único
  
- **Controle de Versões**:
  - Dataset: Versão, data, autor, changelog
  - Modelo: Arquitetura, pesos, métricas, data de treino
  - Código: Git commits, tags de release

**Segurança e Privacidade:**
- Dataset proprietário com controle de acesso (Google Drive com permissões)
- Dados sensíveis não devem ser incluídos em imagens
- Anonimização de metadados quando necessário
- Backup regular (3-2-1: 3 cópias, 2 mídias diferentes, 1 offsite)

### 6.4 Métricas de Sucesso do Projeto

**Métricas Técnicas:**
- ✅ mAP@.50 > 0.70 (Alcançado: 0.789)
- ✅ Tempo de inferência < 100ms (Alcançado: ~30ms)
- ✅ Modelo < 50 MB para deploy (YOLOv5m: 42.2 MB)
- ✅ Dataset > 80 imagens (Exato: 80 imagens)

**Métricas de Processo:**
- ✅ Documentação completa e reprodutível
- ✅ Notebooks executáveis com células narrativas
- ✅ Vídeos demonstrativos publicados
- ✅ Código versionado no GitHub

**Métricas de Negócio (Projetadas):**
- Redução de 50% em tempo de inspeção manual (estimativa)
- Acurácia comparável ou superior a humanos (classe `banana`: 99.5%)
- ROI positivo em 6 meses de operação (projeção)
- Escalabilidade para 10+ classes sem re-arquitetura

### 6.5 Próximos Passos Imediatos

1. **Semana 1-2**: Expandir dataset para 120 imagens (50% increase)
2. **Semana 3-4**: Implementar data augmentation e retreinar modelos
3. **Mês 2**: Iniciar POC de segmentação de instâncias
4. **Mês 3**: Desenvolver API REST para inferência em produção
5. **Trimestre 2**: Integração com primeiro cliente piloto da FarmTech

---

## **7.0 Conclusão**

Este projeto demonstrou com sucesso a viabilidade técnica de soluções de visão computacional para a FarmTech Solutions através de três entregas complementares. A jornada desde detecção básica (Entrega 1), passando por análise comparativa (Entrega 2), até pipeline avançado integrado (Ir Além 2) proporcionou compreensão profunda de trade-offs, limitações e oportunidades em diferentes arquiteturas de Deep Learning.

**Principais Conquistas:**
- Pipeline completo de MLOps desde aquisição de dados até inferência em produção
- Documentação executiva detalhada alinhada com requisitos da Fase 6 da FIAP
- Análise quantitativa e qualitativa de múltiplas arquiteturas e abordagens
- Demonstração prática de transfer learning e integração de modelos

**Impacto para FarmTech Solutions:**
O projeto estabeleceu fundação sólida para expansão de serviços de IA da empresa, validando capacidade técnica da equipe e demonstrando ao cliente fictício o potencial de visão computacional. As recomendações estratégicas fornecem roadmap claro para evolução de POC para produto comercial.

**Alinhamento com Orientações da Fase 6:**
Todas as metas e entregáveis especificados no [`orientation.md`](orientation.md) foram cumpridos integralmente:
- ✅ Dataset com 80 imagens (40 por classe)
- ✅ Divisão estratificada 80/10/10
- ✅ Rotulação no Make Sense AI
- ✅ Múltiplas simulações com diferentes épocas
- ✅ Notebooks com código executado e células Markdown
- ✅ Vídeos demonstrativos no YouTube (não listados)
- ✅ README integrado com notebooks
- ✅ Repositório GitHub público

Este trabalho representa não apenas uma entrega acadêmica, mas uma demonstração profissional de capacidade de execução end-to-end de projetos de Machine Learning, desde concepção até recomendações estratégicas para produção.

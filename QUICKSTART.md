# 🚀 Guia Rápido de Início - FarmTech Solutions

Este guia ajudará você a configurar e executar o sistema FarmTech Solutions em poucos minutos.

## ⚡ Início Rápido (5 minutos)

### 1. Clone e Instale

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/FarmTech_System.git
cd FarmTech_System

# Instale as dependências
pip install -r requirements.txt
```

### 2. Execute o Dashboard

```bash
# Execute o dashboard integrado
streamlit run app_integrated.py
```

O dashboard abrirá automaticamente em: **http://localhost:8501**

### 3. Explore!

Use o menu lateral para navegar entre as fases do projeto.

---

## 📖 Tutoriais por Fase

### 🏠 Fase 1: Visualizar Dados Agrícolas

1. No menu lateral, selecione **"📊 Fase 1: Dados & R"**
2. Visualize estatísticas de produção agrícola
3. Explore os gráficos interativos

### 🤖 Fase 4: Testar Predição de Irrigação

1. Selecione **"🤖 Fase 4: ML Dashboard"**
2. Ajuste os valores dos sensores:
   - Umidade: 25%
   - pH: 6.5
   - Fósforo: Sim
   - Potássio: Sim
3. Clique em **"🚀 Obter Predição"**
4. Veja a recomendação de irrigação e explicação da IA

### ☁️ Fase 5: Testar Sistema de Alertas AWS

1. Selecione **"☁️ Fase 5 & Ir Além 1: AWS"**
2. Escolha o tipo de alerta (ex: "Umidade Baixa")
3. Configure os parâmetros
4. Clique em **"📤 Enviar Alerta"**
5. Observe a simulação do alerta (se AWS não configurado)

### 👁️ Fase 6: Detectar Objetos com YOLO

1. Selecione **"👁️ Fase 6: Visão YOLO"**
2. Faça upload de uma imagem
3. Aguarde a detecção
4. Veja os objetos identificados com bounding boxes
5. Opcionalmente, envie alerta se detectar pragas

### 🧬 Ir Além 2: Otimizar Recursos com Algoritmo Genético

1. Selecione **"🧬 Ir Além 2: Algoritmo Genético"**
2. Configure o orçamento (ex: R$ 150)
3. Ajuste parâmetros do algoritmo (opcional)
4. Clique em **"🎲 Gerar Dados de Culturas"**
5. Clique em **"🚀 Otimizar Recursos"**
6. Veja quais culturas foram selecionadas
7. Analise o gráfico de evolução do fitness

---

## 🔧 Configuração Avançada

### Configurar AWS (Opcional)

Para usar alertas AWS reais ao invés de simulação:

```bash
# Configure suas credenciais AWS
export AWS_ACCESS_KEY_ID=sua_chave_aqui
export AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aqui
export AWS_DEFAULT_REGION=us-east-1
```

### Treinar Novo Modelo de ML

```bash
cd fase_4_dashboard_ml/scripts
python train_model.py
```

### Popular Banco de Dados

```bash
cd fase_4_dashboard_ml/scripts
python populate_db.py
```

---

## 🎯 Casos de Uso Comuns

### Caso 1: Monitorar Irrigação

1. Vá para **Fase 4**
2. Insira dados dos sensores
3. Obtenha predição
4. Se necessário irrigar, vá para **Fase 5**
5. Envie alerta de baixa umidade

### Caso 2: Detectar e Alertar Pragas

1. Vá para **Fase 6**
2. Faça upload de imagem da plantação
3. Aguarde detecção YOLO
4. Se praga detectada, clique em **"Enviar Alerta AWS"**
5. Verifique o alerta enviado

### Caso 3: Otimizar Orçamento de Plantio

1. Vá para **Ir Além 2**
2. Defina seu orçamento disponível
3. Gere dados de culturas disponíveis
4. Execute otimização
5. Veja quais culturas plantar para maximizar retorno

---

## ❓ Solução de Problemas

### Erro: "Module not found"

```bash
# Reinstale as dependências
pip install -r requirements.txt --upgrade
```

### Erro: "Model file not found"

```bash
# Treine o modelo primeiro
cd fase_4_dashboard_ml/scripts
python train_model.py
```

### Dashboard não abre

```bash
# Certifique-se de estar na pasta raiz do projeto
cd /caminho/para/FarmTech_System
streamlit run app_integrated.py
```

### YOLO não funciona

```bash
# Instale PyTorch e Ultralytics
pip install torch torchvision ultralytics
```

---

## 📚 Próximos Passos

Após explorar o dashboard:

1. ✅ Leia o **README_INTEGRATED.md** completo
2. ✅ Explore o código dos módulos:
   - `genetic_optimizer.py`
   - `aws_manager.py`
   - `utils.py`
3. ✅ Execute os scripts individualmente
4. ✅ Customize para suas necessidades

---

## 💡 Dicas

- 🎨 Use **Ctrl + Shift + R** para recarregar o dashboard
- 📊 Gráficos são interativos - clique e explore!
- 🔄 Modo simulação AWS não requer credenciais
- 🧬 Aumente gerações para melhor otimização genética
- 👁️ Use imagens claras para melhor detecção YOLO

---

## 🆘 Precisa de Ajuda?

- 📧 Email: contato@farmtech.com
- 📖 Documentação completa: README_INTEGRATED.md
- 🐛 Issues: GitHub Issues
- 💬 Discussões: GitHub Discussions

---

**🌾 FarmTech Solutions - Agricultura de Precisão com IA**

Desenvolvido com ❤️ usando Streamlit, Python, ML e IoT

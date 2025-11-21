"""
FarmTech Solutions - Dashboard Integrado (Fase 7)
Sistema Unificado de Agritech com IA

Este dashboard integra todas as 6 fases do projeto FarmTech Solutions:
- Fase 1: Análise de Dados com R
- Fase 2: Design de Banco de Dados
- Fase 3: IoT com ESP32
- Fase 4: Dashboard e Machine Learning
- Fase 5: Integração AWS
- Fase 6: Visão Computacional com YOLO
- Ir Além 1: Serviço de Mensageria AWS
- Ir Além 2: Otimização com Algoritmos Genéticos
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import sqlite3
import joblib
from PIL import Image
import matplotlib.pyplot as plt

# Adiciona o diretório de scripts ao path
sys.path.append(str(Path(__file__).parent / 'fase_4_dashboard_ml' / 'scripts'))

# Importa módulos customizados
try:
    from fase_4_dashboard_ml.scripts.utils import load_model, make_prediction, plot_feature_importance
    from ir_alem_2_genetic_algorithm.genetic_optimizer import FarmGeneticOptimizer, generate_sample_farm_items
    from fase_4_dashboard_ml.scripts.aws_manager import AWSManager, AlertLevel
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.info("Execute: pip install -r requirements.txt")

# Configuração da página
st.set_page_config(
    page_title="FarmTech Solutions - Sistema Integrado",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .phase-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1B5E20;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-left: 5px solid #4CAF50;
        background-color: #E8F5E9;
    }
    .metric-card {
        background-color: #F1F8E9;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #AED581;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-info {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .alert-success {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
    }
    .alert-warning {
        background-color: #FFF3E0;
        border-left: 4px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<div class="main-header">🌾 FarmTech Solutions - Sistema Integrado de Agritech com IA</div>', 
            unsafe_allow_html=True)

# Sidebar - Navegação
st.sidebar.title("📋 Navegação")
st.sidebar.markdown("---")

fase = st.sidebar.radio(
    "Selecione a Fase:",
    [
        "🏠 Home",
        "📊 Fase 1: Dados & R",
        "🗄️ Fase 2: Banco de Dados",
        "🔌 Fase 3: IoT ESP32",
        "🤖 Fase 4: ML Dashboard",
        "☁️ Fase 5 & Ir Além 1: AWS",
        "👁️ Fase 6: Visão YOLO",
        "🧬 Ir Além 2: Algoritmo Genético"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**FarmTech Solutions**  
Sistema completo de agricultura de precisão com IA

📧 Contato: contato@farmtech.com  
🌐 Website: www.farmtech.com
""")

# ============================================
# FASE: HOME
# ============================================
if fase == "🏠 Home":
    st.markdown('<div class="phase-header">🏠 Bem-vindo ao FarmTech Solutions</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📁 Fases Implementadas", "6")
    with col2:
        st.metric("🚀 Desafios 'Ir Além'", "2")
    with col3:
        st.metric("🤖 Modelos de IA", "2")
    
    st.markdown("---")
    
    st.markdown("""
    ## 🌟 Sobre o Projeto
    
    O **FarmTech Solutions** é um sistema completo de agricultura de precisão que integra:
    
    - 📊 **Análise de Dados**: Processamento estatístico de dados agrícolas
    - 🗄️ **Banco de Dados**: Sistema robusto de armazenamento
    - 🔌 **IoT**: Monitoramento em tempo real com ESP32
    - 🤖 **Machine Learning**: Predição inteligente de irrigação
    - ☁️ **Cloud AWS**: Infraestrutura escalável e alertas
    - 👁️ **Visão Computacional**: Detecção de pragas com YOLO
    - 🧬 **Otimização**: Algoritmos genéticos para alocação de recursos
    
    ## 🎯 Objetivos do Sistema
    
    1. **Aumentar a eficiência** do uso de recursos hídricos
    2. **Reduzir perdas** por pragas e doenças
    3. **Otimizar alocação** de recursos agrícolas
    4. **Prover insights** baseados em dados
    
    ## 📹 Vídeo de Apresentação
    """)
    
    st.info("🎬 Vídeo de apresentação do projeto (placeholder)")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    st.markdown("---")
    
    st.markdown("""
    ## 🚀 Como Usar
    
    1. **Navegue** pelas fases usando o menu lateral
    2. **Explore** os dados e visualizações de cada fase
    3. **Teste** os modelos de IA interativamente
    4. **Experimente** as funcionalidades de otimização
    
    **💡 Dica:** Comece pela Fase 1 para entender o contexto dos dados!
    """)

# ============================================
# FASE 1: Dados & R
# ============================================
elif fase == "📊 Fase 1: Dados & R":
    st.markdown('<div class="phase-header">📊 Fase 1: Análise de Dados Agrícolas</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase apresenta análise estatística de dados agrícolas do Brasil,
    focando em produção e produtividade por estado.
    """)
    
    # Carrega dados CSV
    csv_path = Path("fase_1_R_analysis/data/agro_data.csv")
    
    if csv_path.exists():
        try:
            # Lê o CSV com separador de ponto e vírgula
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            
            st.success(f"✅ Dados carregados: {len(df)} estados")
            
            # Mostra primeiras linhas
            st.subheader("📋 Primeiras Linhas do Dataset")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Estatísticas descritivas
            st.subheader("📈 Estatísticas Descritivas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "🌾 Área Total Plantada",
                    f"{df['Area Plantada (ha)'].sum():,.0f} ha"
                )
                st.metric(
                    "📊 Produção Total",
                    f"{df['Producao (toneladas)'].sum():,.0f} ton"
                )
            
            with col2:
                st.metric(
                    "📍 Estados Analisados",
                    len(df)
                )
                produtividade_media = df['Producao (toneladas)'].sum() / df['Area Plantada (ha)'].sum()
                st.metric(
                    "⚡ Produtividade Média",
                    f"{produtividade_media:.2f} ton/ha"
                )
            
            # Gráficos
            st.subheader("📊 Visualizações")
            
            tab1, tab2, tab3 = st.tabs(["Top 10 Estados", "Classificação", "Distribuição"])
            
            with tab1:
                # Top 10 estados por produção
                top_10 = df.nlargest(10, 'Producao (toneladas)')
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(top_10['Estado'], top_10['Producao (toneladas)'] / 1_000_000, color='#4CAF50')
                ax.set_xlabel('Produção (Milhões de toneladas)', fontsize=12)
                ax.set_ylabel('Estado', fontsize=12)
                ax.set_title('Top 10 Estados por Produção', fontsize=14, fontweight='bold')
                ax.grid(axis='x', alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
            
            with tab2:
                # Distribuição por classificação
                class_counts = df['Classificacao de Produtividade'].value_counts()
                
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%',
                       colors=['#4CAF50', '#FFC107', '#F44336'], startangle=90)
                ax.set_title('Distribuição por Classificação de Produtividade', 
                            fontsize=14, fontweight='bold')
                st.pyplot(fig)
            
            with tab3:
                # Scatter plot: Área vs Produção
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(
                    df['Area Plantada (ha)'] / 1_000_000,
                    df['Producao (toneladas)'] / 1_000_000,
                    c=df['Classificacao de Produtividade'].map({'Alta': 0, 'Media': 1, 'Baixa': 2}),
                    cmap='RdYlGn_r',
                    s=100,
                    alpha=0.6
                )
                ax.set_xlabel('Área Plantada (Milhões de ha)', fontsize=12)
                ax.set_ylabel('Produção (Milhões de toneladas)', fontsize=12)
                ax.set_title('Relação Área vs Produção', fontsize=14, fontweight='bold')
                ax.grid(alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados: {e}")
    else:
        st.warning(f"⚠️ Arquivo não encontrado: {csv_path}")

# ============================================
# FASE 2: Banco de Dados
# ============================================
elif fase == "🗄️ Fase 2: Banco de Dados":
    st.markdown('<div class="phase-header">🗄️ Fase 2: Design de Banco de Dados</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase apresenta o modelo de banco de dados relacional desenvolvido
    para o sistema FarmTech Solutions.
    """)
    
    # Mostra DER
    der_path = Path("fase_2_database_design/docs/der_farmtech_solutions.png")
    
    if der_path.exists():
        st.subheader("📐 Diagrama Entidade-Relacionamento (DER)")
        image = Image.open(der_path)
        st.image(image, caption="DER FarmTech Solutions", use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("📊 Estrutura do Banco de Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Principais Entidades:**
            - 🌾 **Fazendas**: Informações das propriedades
            - 🌱 **Culturas**: Tipos de cultivo
            - 📊 **Sensores**: Dados de IoT
            - 💧 **Irrigação**: Histórico de acionamentos
            - 🐛 **Pragas**: Detecções de YOLO
            """)
        
        with col2:
            st.markdown("""
            **Relacionamentos:**
            - Fazendas → Culturas (1:N)
            - Culturas → Sensores (1:N)
            - Sensores → Irrigação (1:N)
            - Culturas → Pragas (1:N)
            """)
        
        # Mostra tabela de exemplo
        st.subheader("📋 Exemplo de Dados (irrigation_data)")
        
        db_path = Path("fase_4_dashboard_ml/irrigation.db")
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                query = "SELECT * FROM irrigation_data ORDER BY timestamp DESC LIMIT 10"
                df_db = pd.read_sql_query(query, conn)
                conn.close()
                
                st.dataframe(df_db, use_container_width=True)
                st.success(f"✅ {len(df_db)} registros mostrados")
                
            except Exception as e:
                st.error(f"❌ Erro ao acessar banco: {e}")
        else:
            st.info("💡 Execute o script populate_db.py para gerar dados de exemplo")
    else:
        st.warning(f"⚠️ Imagem DER não encontrada: {der_path}")

# ============================================
# FASE 3: IoT ESP32
# ============================================
elif fase == "🔌 Fase 3: IoT ESP32":
    st.markdown('<div class="phase-header">🔌 Fase 3: Sistema IoT com ESP32</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase implementa um sistema de monitoramento e irrigação automática
    usando ESP32 com sensores de umidade, pH e nutrientes.
    """)
    
    # Mostra código do firmware
    st.subheader("💻 Código do Firmware (prog1.ino)")
    
    firmware_path = Path("fase_3_iot_esp32/prog1.ino")
    if firmware_path.exists():
        with open(firmware_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        st.code(code, language='cpp', line_numbers=True)
        
        st.markdown("---")
        
        # Informações sobre o circuito
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Componentes Utilizados")
            st.markdown("""
            - **ESP32**: Microcontrolador principal
            - **DHT22**: Sensor de umidade e temperatura
            - **LDR**: Simula sensor de pH
            - **Botões**: Simulam sensores de nutrientes
            - **LCD I2C**: Display de informações
            - **Relé**: Controle da bomba de irrigação
            """)
        
        with col2:
            st.subheader("⚙️ Funcionalidades")
            st.markdown("""
            - ✅ Leitura de umidade do solo
            - ✅ Medição de pH
            - ✅ Detecção de nutrientes (P, K)
            - ✅ Acionamento automático de bomba
            - ✅ Display LCD com informações
            - ✅ Comunicação serial
            """)
        
        # Mostra diagram.json se existir
        diagram_path = Path("fase_3_iot_esp32/diagram.json")
        if diagram_path.exists():
            with st.expander("🔍 Ver Configuração Wokwi (diagram.json)"):
                with open(diagram_path, 'r') as f:
                    diagram_code = f.read()
                st.code(diagram_code, language='json')
    else:
        st.warning(f"⚠️ Arquivo não encontrado: {firmware_path}")

# ============================================
# FASE 4: ML Dashboard
# ============================================
elif fase == "🤖 Fase 4: ML Dashboard":
    st.markdown('<div class="phase-header">🤖 Fase 4: Machine Learning - Predição de Irrigação</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase implementa um modelo de Machine Learning (Random Forest) para
    prever a necessidade de irrigação com base em dados dos sensores.
    """)
    
    # Carrega modelo
    model_path = Path("fase_4_dashboard_ml/irrigation_model.joblib")
    
    if model_path.exists():
        model = load_model(str(model_path))
        
        if model is not None:
            st.success("✅ Modelo carregado com sucesso!")
            
            # Métricas do modelo
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tipo de Modelo", "Random Forest")
            with col2:
                st.metric("Acurácia", "98.5%")
            with col3:
                st.metric("Features", "4")
            with col4:
                st.metric("Versão", "v1.0")
            
            st.markdown("---")
            
            # Interface de predição
            st.subheader("🎯 Fazer Predição")
            
            col1, col2 = st.columns(2)
            
            with col1:
                humidity = st.slider('Umidade do Solo (%)', 0, 100, 50, 1)
                ph = st.slider('pH do Solo', 0.0, 14.0, 7.0, 0.1)
            
            with col2:
                phosphorus = st.selectbox('Fósforo Presente', [0, 1], index=1, 
                                         format_func=lambda x: "Sim" if x == 1 else "Não")
                potassium = st.selectbox('Potássio Presente', [0, 1], index=1,
                                        format_func=lambda x: "Sim" if x == 1 else "Não")
            
            if st.button('🚀 Obter Predição', type="primary"):
                # Prepara dados
                input_data = pd.DataFrame({
                    'humidity': [humidity],
                    'phosphorus': [phosphorus],
                    'potassium': [potassium],
                    'ph': [ph]
                })
                
                # Faz predição
                prediction_label, confidence = make_prediction(model, input_data)
                
                # Mostra resultado
                st.markdown("---")
                st.subheader("📊 Resultado da Predição")
                
                if prediction_label == "IRRIGATE":
                    st.success(f"💧 **{prediction_label}**")
                    st.info(f"**Confiança:** {confidence}")
                    st.markdown("💡 **Recomendação:** Ativar sistema de irrigação")
                else:
                    st.info(f"🚫 **{prediction_label}**")
                    st.success(f"**Confiança:** {confidence}")
                    st.markdown("💡 **Recomendação:** Irrigação não necessária no momento")
                
                # Explicabilidade
                st.markdown("---")
                st.subheader("🧠 Explicabilidade da IA")
                
                feature_names = ['humidity', 'phosphorus', 'potassium', 'ph']
                plot_feature_importance(model, feature_names)
                
                st.markdown("""
                **📚 Interpretação:**
                - **Barras maiores** = características mais importantes
                - **Humidity**: Fator mais crítico para irrigação
                - **pH**: Afeta absorção de nutrientes
                - **Nutrientes**: Influenciam necessidade de água
                """)
    else:
        st.warning(f"⚠️ Modelo não encontrado: {model_path}")
        st.info("💡 Execute: python fase_4_dashboard_ml/scripts/train_model.py")

# ============================================
# FASE 5 & IR ALÉM 1: AWS
# ============================================
elif fase == "☁️ Fase 5 & Ir Além 1: AWS":
    st.markdown('<div class="phase-header">☁️ Fase 5: Infraestrutura AWS & Sistema de Alertas</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase apresenta a infraestrutura AWS proposta e implementa
    um sistema de alertas via SNS (Simple Notification Service).
    """)
    
    # Mostra comparação de custos
    st.subheader("💰 Comparação de Custos AWS")
    
    cost_img_path = Path("fase_5_aws_docs/docs/aws_comparison_cost.png")
    if cost_img_path.exists():
        image = Image.open(cost_img_path)
        st.image(image, caption="Análise de Custos AWS", use_container_width=True)
    else:
        st.warning(f"⚠️ Imagem não encontrada: {cost_img_path}")
    
    st.markdown("---")
    
    # Sistema de alertas
    st.subheader("🔔 Sistema de Alertas AWS SNS")
    
    # Inicializa AWS Manager
    aws_manager = AWSManager()
    
    # Mostra status
    status = aws_manager.get_status()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "AWS Configurado",
            "✅ Sim" if status['aws_configured'] else "❌ Não"
        )
    with col2:
        st.metric(
            "Modo",
            "🔄 Simulação" if status['simulate_mode'] else "☁️ Real"
        )
    with col3:
        st.metric("Região", status['region'])
    
    st.markdown("---")
    
    # Interface para testar alertas
    st.subheader("🧪 Testar Sistema de Alertas")
    
    alert_type = st.selectbox(
        "Tipo de Alerta",
        ["Umidade Baixa", "Detecção de Praga", "Alerta Genérico"]
    )
    
    if alert_type == "Umidade Baixa":
        col1, col2 = st.columns(2)
        with col1:
            test_humidity = st.number_input("Umidade Atual (%)", 0, 100, 25)
        with col2:
            threshold = st.number_input("Limite Mínimo (%)", 0, 100, 30)
        
        if st.button("📤 Enviar Alerta de Umidade", type="primary"):
            result = aws_manager.send_soil_moisture_alert(test_humidity, threshold)
            if result['success']:
                st.success("✅ Alerta enviado com sucesso!")
                st.json(result)
            else:
                st.error("❌ Erro ao enviar alerta")
    
    elif alert_type == "Detecção de Praga":
        col1, col2 = st.columns(2)
        with col1:
            pest_name = st.text_input("Nome da Praga", "Lagarta")
        with col2:
            pest_confidence = st.slider("Confiança (%)", 0, 100, 85)
        
        location = st.text_input("Localização", "Setor A - Plantação de Soja")
        
        if st.button("📤 Enviar Alerta de Praga", type="primary"):
            result = aws_manager.send_pest_detection_alert(
                pest_name,
                pest_confidence,
                location
            )
            if result['success']:
                st.success("✅ Alerta enviado com sucesso!")
                st.json(result)
            else:
                st.error("❌ Erro ao enviar alerta")
    
    else:  # Alerta Genérico
        alert_title = st.text_input("Título do Alerta", "Manutenção Programada")
        alert_details = st.text_area("Detalhes", "Sistema será desligado para manutenção")
        alert_level = st.selectbox("Nível", ["INFO", "WARNING", "CRITICAL", "EMERGENCY"])
        
        if st.button("📤 Enviar Alerta Genérico", type="primary"):
            result = aws_manager.send_system_alert(
                alert_title,
                alert_details,
                AlertLevel[alert_level]
            )
            if result['success']:
                st.success("✅ Alerta enviado com sucesso!")
                st.json(result)
            else:
                st.error("❌ Erro ao enviar alerta")

# ============================================
# FASE 6: Visão YOLO
# ============================================
elif fase == "👁️ Fase 6: Visão YOLO":
    st.markdown('<div class="phase-header">👁️ Fase 6: Visão Computacional com YOLO</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase implementa detecção de objetos usando YOLOv5, treinado
    para identificar pragas e outros elementos na plantação.
    """)
    
    # Verifica se modelo YOLO existe
    yolo_model_path = Path("fase_6_vision_yolo/best.pt")
    
    if yolo_model_path.exists():
        st.success("✅ Modelo YOLO encontrado!")
        
        # Informações do modelo
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Arquitetura", "YOLOv5")
        with col2:
            st.metric("Classes", "2")
        with col3:
            st.metric("mAP@0.5", "51.3%")
        with col4:
            st.metric("Épocas", "60")
        
        st.markdown("---")
        
        # Upload de imagem
        st.subheader("📸 Detecção de Objetos")
        
        uploaded_file = st.file_uploader(
            "Faça upload de uma imagem",
            type=['jpg', 'jpeg', 'png'],
            help="Envie uma imagem para detectar objetos"
        )
        
        if uploaded_file is not None:
            # Mostra imagem original
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📷 Imagem Original")
                st.image(image, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Detecções")
                
                # Aqui você carregaria o modelo YOLO e faria a detecção
                # Por ora, mostramos um placeholder
                st.info("🔄 Processando com YOLO...")
                
                try:
                    import torch
                    
                    # Carrega modelo
                    model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                          path=str(yolo_model_path), force_reload=False)
                    
                    # Faz detecção
                    results = model(image)
                    
                    # Mostra resultados
                    st.image(results.render()[0], use_container_width=True)
                    
                    # Informações das detecções
                    detections = results.pandas().xyxy[0]
                    
                    if len(detections) > 0:
                        st.success(f"✅ {len(detections)} objeto(s) detectado(s)!")
                        st.dataframe(detections[['name', 'confidence']], use_container_width=True)
                        
                        # Verifica se detectou praga e envia alerta
                        for _, det in detections.iterrows():
                            if det['confidence'] > 0.7:  # Alta confiança
                                st.warning(f"⚠️ Detecção com alta confiança: {det['name']}")
                                
                                if st.button(f"📤 Enviar Alerta AWS para {det['name']}"):
                                    aws_manager = AWSManager()
                                    result = aws_manager.send_pest_detection_alert(
                                        pest_type=det['name'],
                                        confidence=det['confidence'] * 100,
                                        location="Área monitorada"
                                    )
                                    if result['success']:
                                        st.success("✅ Alerta enviado!")
                    else:
                        st.info("ℹ️ Nenhum objeto detectado")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao carregar modelo YOLO: {e}")
                    st.info("💡 Certifique-se de que PyTorch e Ultralytics estão instalados")
                    st.code("pip install torch torchvision ultralytics")
        
        else:
            st.info("📤 Faça upload de uma imagem para começar a detecção")
    
    else:
        st.warning(f"⚠️ Modelo YOLO não encontrado: {yolo_model_path}")
        st.info("💡 Treine o modelo YOLO primeiro usando o notebook da Fase 6")

# ============================================
# IR ALÉM 2: Algoritmo Genético
# ============================================
elif fase == "🧬 Ir Além 2: Algoritmo Genético":
    st.markdown('<div class="phase-header">🧬 Ir Além 2: Otimização com Algoritmo Genético</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase implementa um **Algoritmo Genético** para otimizar a alocação
    de recursos agrícolas, resolvendo o problema da mochila binária aplicado
    ao contexto de culturas e orçamento limitado.
    """)
    
    # Configurações
    st.subheader("⚙️ Configurações da Otimização")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget = st.slider("💰 Orçamento Disponível (R$)", 50, 500, 150, 10)
        num_items = st.slider("🌾 Número de Culturas", 5, 30, 20, 1)
    
    with col2:
        population_size = st.slider("👥 Tamanho da População", 8, 64, 16, 8)
        num_generations = st.slider("🔄 Número de Gerações", 100, 2000, 500, 100)
    
    with col3:
        crossover_rate = st.slider("🧬 Taxa de Crossover", 0.0, 1.0, 0.8, 0.1)
        mutation_rate = st.slider("🎲 Taxa de Mutação", 0.0, 0.5, 0.15, 0.05)
    
    st.markdown("---")
    
    # Gera dados de culturas
    if st.button("🎲 Gerar Dados de Culturas", type="secondary"):
        st.session_state['farm_items'] = generate_sample_farm_items(num_items)
    
    # Mostra tabela de culturas
    if 'farm_items' not in st.session_state:
        st.session_state['farm_items'] = generate_sample_farm_items(num_items)
    
    st.subheader("🌱 Culturas Disponíveis")
    st.dataframe(st.session_state['farm_items'], use_container_width=True)
    
    # Estatísticas das culturas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Custo Total", f"R$ {st.session_state['farm_items']['Custo'].sum()}")
    with col2:
        st.metric("💎 Valor Total", f"R$ {st.session_state['farm_items']['Valor'].sum()}")
    with col3:
        ratio = st.session_state['farm_items']['Valor'].sum() / st.session_state['farm_items']['Custo'].sum()
        st.metric("📊 Razão Valor/Custo", f"{ratio:.2f}")
    
    st.markdown("---")
    
    # Botão de otimização
    if st.button("🚀 Otimizar Recursos", type="primary"):
        with st.spinner("🧬 Executando algoritmo genético..."):
            try:
                # Cria otimizador
                optimizer = FarmGeneticOptimizer(
                    items_df=st.session_state['farm_items'],
                    budget=budget,
                    population_size=population_size,
                    num_generations=num_generations,
                    crossover_rate=crossover_rate,
                    mutation_rate=mutation_rate
                )
                
                # Executa otimização
                selected_items, total_value, total_cost, history = optimizer.optimize()
                
                # Mostra resultados
                st.success("✅ Otimização concluída!")
                
                st.markdown("---")
                st.subheader("📊 Resultados da Otimização")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🌾 Culturas Selecionadas", len(selected_items))
                with col2:
                    st.metric("💎 Valor Total", f"R$ {total_value}")
                with col3:
                    st.metric("💰 Custo Total", f"R$ {total_cost}")
                with col4:
                    st.metric("📊 Utilização", f"{total_cost/budget*100:.1f}%")
                
                # Lista de itens selecionados
                st.subheader("✅ Culturas Selecionadas para Plantio")
                
                selected_df = st.session_state['farm_items'][
                    st.session_state['farm_items']['Nome'].isin(selected_items)
                ]
                st.dataframe(selected_df, use_container_width=True)
                
                # Gráfico de evolução
                st.subheader("📈 Evolução do Fitness")
                
                fig = optimizer.plot_fitness_evolution(figsize=(12, 6))
                st.pyplot(fig)
                
                # Insights
                st.subheader("💡 Insights")
                
                efficiency = (total_value / total_cost) if total_cost > 0 else 0
                budget_usage = (total_cost / budget) * 100
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Eficiência da Solução:**
                    - Razão Valor/Custo: **{efficiency:.2f}**
                    - Uso do orçamento: **{budget_usage:.1f}%**
                    - Valor médio por cultura: **R$ {total_value/len(selected_items):.2f}**
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Desempenho do Algoritmo:**
                    - Gerações executadas: **{num_generations}**
                    - População: **{population_size} indivíduos**
                    - Fitness final: **{total_value}**
                    """)
                
            except Exception as e:
                st.error(f"❌ Erro na otimização: {e}")
                import traceback
                st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>🌾 FarmTech Solutions v1.0</strong></p>
    <p>Sistema Integrado de Agricultura de Precisão com IA</p>
    <p>Desenvolvido com ❤️ usando Streamlit, Python, ML e IoT</p>
</div>
""", unsafe_allow_html=True)

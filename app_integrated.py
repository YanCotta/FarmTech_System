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

# Configuração da página (DEVE SER A PRIMEIRA CHAMADA STREAMLIT)
st.set_page_config(
    page_title="FarmTech Solutions - Sistema Integrado",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import sqlite3
import joblib
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO, StringIO

# Adiciona os diretórios ao path
sys.path.append(str(Path(__file__).parent / 'fase_4_dashboard_ml' / 'scripts'))
sys.path.append(str(Path(__file__).parent / 'ir_alem_2_genetic_algorithm'))

# Funções de cache para modelos
@st.cache_resource
def load_ml_model(model_path):
    """Carrega modelo de ML com cache"""
    try:
        import joblib
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Erro ao carregar modelo ML: {e}")
        return None

@st.cache_resource
def load_yolo_model(model_path):
    """Carrega modelo YOLO com cache"""
    try:
        import torch
        model = torch.hub.load('ultralytics/yolov5', 'custom', 
                              path=str(model_path), force_reload=False)
        return model
    except Exception as e:
        st.error(f"Erro ao carregar modelo YOLO: {e}")
        return None

# Importa módulos customizados
try:
    from fase_4_dashboard_ml.scripts.utils import load_model, make_prediction, plot_feature_importance
    from genetic_optimizer import FarmGeneticOptimizer, generate_sample_farm_items
    from fase_4_dashboard_ml.scripts.aws_manager import AWSAlertManager, AWSManager, AlertLevel
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.info("Execute: pip install -r requirements.txt")
    st.stop()

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

@st.cache_data
def generate_sensor_locations(num_sensors=20):
    """
    Gera localização fictícia de sensores em região agrícola.
    Região: Ribeirão Preto - SP (principal polo de agronegócio)
    """
    # Centro: Ribeirão Preto, SP
    center_lat = -21.1767
    center_lon = -47.8208
    
    # Gera pontos aleatórios em um raio de ~10km
    np.random.seed(42)
    locations = []
    
    for i in range(num_sensors):
        # Offset aleatório (aproximadamente 0.1 grau = ~11km)
        lat_offset = np.random.uniform(-0.08, 0.08)
        lon_offset = np.random.uniform(-0.08, 0.08)
        
        locations.append({
            'sensor_id': f'ESP32-{i+1:03d}',
            'lat': center_lat + lat_offset,
            'lon': center_lon + lon_offset,
            'humidity': np.random.uniform(15, 60),
            'ph': np.random.uniform(5.5, 8.5),
            'sector': f'Setor {chr(65 + i % 6)}'  # A, B, C, D, E, F
        })
    
    return pd.DataFrame(locations)

def create_download_csv(df, filename):
    """Gera botão de download CSV"""
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
        key=f"download_{filename}"
    )

# CSS Profissional - Clean Corporate Theme
st.markdown("""
<style>
    /* Reset e Variáveis */
    :root {
        --primary-green: #2E7D32;
        --secondary-green: #388E3C;
        --light-gray: #F5F5F5;
        --medium-gray: #E0E0E0;
        --dark-gray: #333333;
        --white: #FFFFFF;
        --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
    
    /* Header Principal */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: var(--white);
        text-align: center;
        padding: 1.5rem 2rem;
        background: var(--primary-green);
        border-radius: 4px;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }
    
    /* Headers de Fase */
    .phase-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--dark-gray);
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-green);
    }
    
    /* Cards de Métricas */
    .metric-card {
        background-color: var(--white);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow);
        transition: box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-hover);
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 1rem 1.5rem;
        border-radius: 4px;
        margin: 1rem 0;
        background-color: var(--light-gray);
        border-left: 4px solid var(--primary-green);
    }
    
    .alert-info {
        background-color: #E3F2FD;
        border-left-color: #1976D2;
    }
    
    .alert-success {
        background-color: #E8F5E9;
        border-left-color: var(--primary-green);
    }
    
    .alert-warning {
        background-color: #FFF3E0;
        border-left-color: #F57C00;
    }
    
    /* Containers */
    .stApp {
        background-color: var(--light-gray);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--white);
        border-right: 1px solid var(--medium-gray);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--primary-green);
        color: var(--white);
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--secondary-green);
    }
    
    /* Tabelas */
    .dataframe {
        border: 1px solid var(--medium-gray) !important;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<div class="main-header">FarmTech Solutions | Sistema Integrado de Agricultura de Precisão</div>', 
            unsafe_allow_html=True)

# Sidebar - Navegação
st.sidebar.title("Navegação")
st.sidebar.markdown("---")

fase = st.sidebar.radio(
    "Selecione o Módulo:",
    [
        "Visão Geral",
        "Fase 1: Análise de Dados",
        "Fase 2: Banco de Dados",
        "Fase 3: IoT ESP32",
        "Fase 4: Machine Learning",
        "Fase 5: AWS & Alertas",
        "Fase 6: Visão Computacional",
        "Otimização Genética",
        "Assistente IA"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**FarmTech Solutions**  
Sistema de Agricultura de Precisão

Desenvolvido para FIAP - Fase 7  
RM562836 - Yan Pimentel Cotta
""")

# ============================================
# MÓDULO: VISÃO GERAL
# ============================================
if fase == "Visão Geral":
    st.markdown('<div class="phase-header">Visão Geral do Sistema</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fases Implementadas", "6")
    with col2:
        st.metric("Módulos Extras", "2")
    with col3:
        st.metric("Modelos de IA", "2")
    
    st.markdown("---")
    
    st.markdown("""
    ### Sobre o Projeto
    
    O **FarmTech Solutions** é um sistema integrado de agricultura de precisão desenvolvido 
    como projeto final do curso de IA da FIAP, integrando 6 fases principais e 2 desafios extras.
    
    **Módulos Implementados:**
    
    - **Análise de Dados**: Processamento estatístico de dados agrícolas com R
    - **Banco de Dados**: Modelo relacional completo para gestão de dados
    - **IoT ESP32**: Monitoramento em tempo real de sensores agrícolas
    - **Machine Learning**: Predição inteligente de necessidade de irrigação
    - **Cloud AWS**: Sistema de alertas via SNS com fallback de simulação
    - **Visão Computacional**: Detecção de pragas utilizando YOLOv5
    - **Otimização Genética**: Alocação ótima de recursos com algoritmos genéticos
    
    ### Objetivos Técnicos
    
    1. Aumentar a eficiência do uso de recursos hídricos
    2. Reduzir perdas agrícolas causadas por pragas e doenças
    3. Otimizar a alocação de recursos dentro de restrições orçamentárias
    4. Fornecer insights baseados em análise de dados e inteligência artificial
    
    ### Guia de Uso
    
    1. Navegue pelas fases usando o menu lateral
    2. Explore os dados e visualizações de cada módulo
    3. Teste os modelos de IA de forma interativa
    4. Experimente as funcionalidades de otimização
    """)

# ============================================
# FASE 1: Dados & R
# ============================================
elif fase == "Fase 1: Análise de Dados":
    st.markdown('<div class="phase-header">Fase 1: Análise de Dados Agrícolas</div>', 
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
elif fase == "Fase 2: Banco de Dados":
    st.markdown('<div class="phase-header">Fase 2: Design de Banco de Dados</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase apresenta o modelo de banco de dados relacional desenvolvido
    para o sistema FarmTech Solutions.
    """)
    
    # Tenta localizar a imagem DER
    der_path = Path("fase_2_database_design/docs/der_farmtech_solutions.png")
    
    # Se não existir, tenta outros nomes possíveis
    if not der_path.exists():
        possible_paths = [
            Path("fase_2_database_design/docs/DER_FarmTech.png"),
            Path("fase_2_database_design/docs/database_diagram.png"),
            Path("assets/der_farmtech.png")
        ]
        for p in possible_paths:
            if p.exists():
                der_path = p
                break
    
    if der_path.exists():
        st.subheader("📐 Diagrama Entidade-Relacionamento (DER)")
        image = Image.open(der_path)
        st.image(image, caption="DER FarmTech Solutions", use_column_width=True)
        
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
elif fase == "Fase 3: IoT ESP32":
    st.markdown('<div class="phase-header">Fase 3: Sistema IoT com ESP32</div>', 
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
elif fase == "Fase 4: Machine Learning":
    st.markdown('<div class="phase-header">Fase 4: Machine Learning - Predição de Irrigação</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase implementa um modelo de Machine Learning (Random Forest) para
    prever a necessidade de irrigação com base em dados dos sensores.
    """)
    
    # Carrega modelo com cache
    model_path = Path("fase_4_dashboard_ml/irrigation_model.joblib")
    
    if model_path.exists():
        model = load_ml_model(str(model_path))
        
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
elif fase == "Fase 5: AWS & Alertas":
    st.markdown('<div class="phase-header">Fase 5: Infraestrutura AWS e Sistema de Alertas</div>',
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
        st.image(image, caption="Análise de Custos AWS", use_column_width=True)
    else:
        st.warning(f"⚠️ Imagem não encontrada: {cost_img_path}")
    
    st.markdown("---")
    
    # Sistema de alertas
    st.subheader("🔔 Sistema de Alertas AWS SNS (Nova Versão - v2.0)")
    
    # Inicializa AWS Alert Manager (nova versão)
    if 'aws_manager' not in st.session_state:
        st.session_state.aws_manager = AWSAlertManager()
    
    aws_manager = st.session_state.aws_manager
    
    # Mostra status
    stats = aws_manager.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Modo de Operação",
            "🔄 Simulação" if aws_manager.simulation_mode else "☁️ AWS Real"
        )
    with col2:
        st.metric(
            "Alertas Enviados",
            stats['total_sent']
        )
    with col3:
        st.metric(
            "Taxa de Sucesso",
            f"{stats['success_rate']:.1f}%"
        )
    
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
            result = aws_manager.notify_low_humidity(
                humidity_value=test_humidity,
                threshold=threshold,
                location="Teste via Dashboard"
            )
            if result['success']:
                st.success("✅ Alerta enviado com sucesso!")
                with st.expander("📋 Detalhes do Envio"):
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
            result = aws_manager.notify_pest_detection(
                pest_name=pest_name,
                confidence=pest_confidence / 100,  # Converte de % para 0-1
                location=location
            )
            if result['success']:
                st.success("✅ Alerta enviado com sucesso!")
                with st.expander("📋 Detalhes do Envio"):
                    st.json(result)
            else:
                st.error("❌ Erro ao enviar alerta")
    
    else:  # Alerta Genérico
        alert_title = st.text_input("Título do Alerta", "Manutenção Programada")
        alert_details = st.text_area("Detalhes", "Sistema será desligado para manutenção")
        alert_level = st.selectbox("Nível", ["INFO", "WARNING", "CRITICAL", "EMERGENCY"])
        
        if st.button("📤 Enviar Alerta Genérico", type="primary"):
            from fase_4_dashboard_ml.scripts.aws_manager import AlertType, AlertLevel as AL
            result = aws_manager.send_alert(
                subject=alert_title,
                message=alert_details,
                alert_type=AlertType.CUSTOM,
                severity=AL[alert_level]
            )
            if result['success']:
                st.success("✅ Alerta enviado com sucesso!")
                with st.expander("📋 Detalhes do Envio"):
                    st.json(result)
            else:
                st.error("❌ Erro ao enviar alerta")

# ============================================
# FASE 6: Visão YOLO (Enhanced com Multi-Model + LLM Vision)
# ============================================
elif fase == "Fase 6: Visão Computacional":
    st.markdown('<div class="phase-header">Fase 6: Visão Computacional com YOLO + LLM Vision</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta fase implementa **Hybrid AI**: detecção rápida com YOLO (edge) + análise 
    inteligente com LLM Vision (cloud) para diagnóstico fitopatológico avançado.
    """)
    
    # Seleção de modelo
    st.subheader("🤖 Configuração do Modelo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        model_type = st.radio(
            "Selecione o Modelo YOLO:",
            ["Modelo FarmTech (Especializado em Pragas/Bananas)", 
             "YOLOv5s (Detecção Geral - COCO Dataset)"],
            help="FarmTech: treinado para pragas agrícolas | YOLOv5s: 80 classes gerais"
        )
    
    with col2:
        # Checkbox para análise LLM
        llm_analysis = st.checkbox(
            "🧠 Análise Detalhada via LLM Vision",
            help="Requer API Key configurada no Assistente IA"
        )
        
        if llm_analysis:
            llm_api_key = st.text_input(
                "API Key (OpenAI)",
                type="password",
                key="llm_vision_key",
                help="Mesma chave do Assistente IA"
            )
    
    # Carrega modelo baseado na seleção
    if model_type == "Modelo FarmTech (Especializado em Pragas/Bananas)":
        yolo_model_path = Path("fase_6_vision_yolo/best.pt")
        
        if yolo_model_path.exists():
            st.success("✅ Modelo FarmTech carregado!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Arquitetura", "YOLOv5")
            with col2:
                st.metric("Classes", "2 (Pragas)")
            with col3:
                st.metric("mAP@0.5", "51.3%")
            with col4:
                st.metric("Épocas", "60")
            
            model_source = "custom"
            model_path = yolo_model_path
        else:
            st.error(f"❌ Modelo FarmTech não encontrado: {yolo_model_path}")
            st.info("💡 Treine o modelo usando o notebook da Fase 6 ou use o modelo geral")
            model_source = None
            model_path = None
    
    else:  # YOLOv5s General
        st.success("✅ Modelo YOLOv5s (General) selecionado!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Arquitetura", "YOLOv5s")
        with col2:
            st.metric("Classes", "80 (COCO)")
        with col3:
            st.metric("Dataset", "COCO")
        with col4:
            st.metric("Tamanho", "14.1 MB")
        
        model_source = "pretrained"
        model_path = None
    
    st.markdown("---")
    
    # Upload de imagem
    st.subheader("📸 Detecção e Análise")
    
    uploaded_file = st.file_uploader(
        "Faça upload de uma imagem",
        type=['jpg', 'jpeg', 'png'],
        help="Envie uma imagem de planta/cultivo para análise"
    )
    
    if uploaded_file is not None:
        try:
            # Carrega imagem
            from io import BytesIO
            import base64
            
            image = Image.open(BytesIO(uploaded_file.read()))
            uploaded_file.seek(0)
            
            # Layout de 2 colunas
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📷 Imagem Original")
                st.image(image, use_column_width=True)
            
            with col2:
                st.subheader("🎯 Detecções YOLO")
                
                try:
                    # Carrega modelo apropriado
                    if model_source == "custom":
                        model = load_yolo_model(model_path)
                    elif model_source == "pretrained":
                        # Cache do modelo geral
                        if 'yolo_general_model' not in st.session_state:
                            with st.spinner("📥 Baixando YOLOv5s (primeira vez)..."):
                                import torch
                                st.session_state.yolo_general_model = torch.hub.load(
                                    'ultralytics/yolov5', 
                                    'yolov5s',
                                    pretrained=True,
                                    force_reload=False
                                )
                        model = st.session_state.yolo_general_model
                    else:
                        st.error("❌ Nenhum modelo disponível")
                        st.stop()
                    
                    if model is not None:
                        # Faz detecção
                        results = model(image)
                        
                        # Renderiza resultados
                        result_img = results.render()[0]
                        st.image(result_img, use_column_width=True)
                        
                        # Extrai detecções
                        detections = results.pandas().xyxy[0]
                        
                        if len(detections) > 0:
                            st.success(f"✅ {len(detections)} objeto(s) detectado(s)!")
                            
                            # Tabela de detecções
                            st.dataframe(
                                detections[['name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']]
                                .style.format({'confidence': '{:.2%}'}),
                                use_container_width=True
                            )
                            
                            # Alertas AWS para detecções com alta confiança
                            for idx, det in detections.iterrows():
                                if det['confidence'] > 0.7:
                                    st.warning(f"⚠️ Alta confiança: {det['name']} ({det['confidence']*100:.1f}%)")
                                    
                                    if st.button(f"📤 Enviar Alerta AWS", key=f"alert_{idx}"):
                                        if 'aws_manager' not in st.session_state:
                                            st.session_state.aws_manager = AWSAlertManager()
                                        
                                        result = st.session_state.aws_manager.notify_pest_detection(
                                            pest_name=det['name'],
                                            confidence=det['confidence'],
                                            image_path=uploaded_file.name,
                                            location="Dashboard - Análise YOLO"
                                        )
                                        if result['success']:
                                            st.success(f"✅ Alerta enviado! Modo: {result['mode']}")
                        else:
                            st.info("ℹ️ Nenhum objeto detectado pelo YOLO")
                    
                    else:
                        st.error("❌ Falha ao carregar modelo")
                
                except Exception as e:
                    st.error(f"❌ Erro na detecção: {e}")
                    st.code(str(e))
            
            # Análise LLM Vision (se habilitada)
            if llm_analysis and 'llm_api_key' in locals() and llm_api_key:
                st.markdown("---")
                st.subheader("🧠 Análise Fitopatológica via LLM Vision")
                
                with st.spinner("🔬 Analisando imagem com IA generativa..."):
                    try:
                        import requests
                        import base64
                        
                        # Converte imagem para base64
                        buffered = BytesIO()
                        image.save(buffered, format="JPEG")
                        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        
                        # Prompt especializado
                        vision_prompt = """Você é um fitopatologista especializado. Analise esta imagem de planta/cultivo e forneça:

1. **Diagnóstico Visual**: O que você identifica na imagem?
2. **Saúde da Planta**: A planta aparenta estar saudável ou com problemas?
3. **Sintomas Observados**: Descreva manchas, descolorações, pragas visíveis, etc.
4. **Possíveis Doenças/Pragas**: Liste hipóteses diagnósticas
5. **Recomendações**: Ações imediatas sugeridas

Seja técnico mas acessível. Use emojis para destacar pontos importantes."""

                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {llm_api_key}"
                        }
                        
                        payload = {
                            "model": "gpt-4o-mini",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": vision_prompt
                                        },
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:image/jpeg;base64,{img_base64}"
                                            }
                                        }
                                    ]
                                }
                            ],
                            "max_tokens": 1000,
                            "temperature": 0.3
                        }
                        
                        response = requests.post(
                            "https://api.openai.com/v1/chat/completions",
                            headers=headers,
                            json=payload,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            analysis = result['choices'][0]['message']['content']
                            
                            st.markdown("### 📋 Relatório Fitopatológico")
                            st.markdown(analysis)
                            
                            # Metrics de uso
                            usage = result.get('usage', {})
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Tokens Prompt", usage.get('prompt_tokens', 'N/A'))
                            with col2:
                                st.metric("Tokens Resposta", usage.get('completion_tokens', 'N/A'))
                            with col3:
                                st.metric("Total", usage.get('total_tokens', 'N/A'))
                        
                        else:
                            st.error(f"❌ Erro na API: {response.status_code}")
                            st.code(response.text)
                    
                    except Exception as e:
                        st.error(f"❌ Erro na análise LLM: {e}")
            
            elif llm_analysis and (not 'llm_api_key' in locals() or not llm_api_key):
                st.info("💡 Configure a API Key acima para habilitar análise LLM Vision")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar imagem: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    else:
        st.info("📤 Faça upload de uma imagem para começar")
        
        # Preview de capacidades
        with st.expander("🎯 Capacidades do Sistema"):
            st.markdown("""
            **YOLO Edge Detection (Rápido):**
            - ✅ Detecção em tempo real
            - ✅ Múltiplos objetos simultâneos
            - ✅ Bounding boxes precisos
            - ✅ Confiança por detecção
            
            **LLM Vision Analysis (Inteligente):**
            - 🧠 Diagnóstico fitopatológico detalhado
            - 🧠 Identificação de sintomas sutis
            - 🧠 Recomendações de tratamento
            - 🧠 Análise de contexto completo
            
            **Hybrid AI = Melhor dos 2 Mundos!**
            """)

# ============================================
# IR ALÉM 2: Algoritmo Genético
# ============================================
elif fase == "Otimização Genética":
    st.markdown('<div class="phase-header">Otimização com Algoritmo Genético</div>', 
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

# ============================================
# ASSISTENTE IA - Interface de Linguagem Natural
# ============================================
elif fase == "Assistente IA":
    st.markdown('<div class="phase-header">Assistente IA - Consulta em Linguagem Natural</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Converse com seus dados agrícolas em linguagem natural. O assistente analisa
    os dados de sensores e responde perguntas sobre irrigação, pH, nutrientes e muito mais.
    """)
    
    # Configuração de API Key
    st.subheader("🔑 Configuração")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        api_key = st.text_input(
            "API Key (OpenAI)",
            type="password",
            help="Insira sua chave de API da OpenAI. Você pode obtê-la em https://platform.openai.com/api-keys"
        )
    
    with col2:
        model_choice = st.selectbox(
            "Modelo",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            help="gpt-4o-mini é mais rápido e barato"
        )
    
    st.markdown("---")
    
    # Verifica se há API key
    if not api_key:
        st.info("""
        ### 💡 Como usar o Assistente IA
        
        1. **Obtenha uma API Key** da OpenAI em https://platform.openai.com/api-keys
        2. **Cole a chave** no campo acima (ela ficará oculta)
        3. **Faça perguntas** sobre seus dados agrícolas
        
        **Exemplos de perguntas:**
        - "Quais setores precisam de irrigação urgente?"
        - "Qual é o pH médio do solo?"
        - "Existem áreas com déficit de fósforo?"
        - "Qual a umidade mínima registrada?"
        - "Quantos sensores indicam necessidade de irrigação?"
        """)
        
        # Mostra preview dos dados mesmo sem API key
        st.subheader("📊 Preview dos Dados Disponíveis")
        
        db_path = Path("fase_4_dashboard_ml/irrigation.db")
        if db_path.exists():
            try:
                conn = sqlite3.connect(db_path)
                df = pd.read_sql_query("SELECT * FROM irrigation_data ORDER BY id DESC LIMIT 10", conn)
                conn.close()
                
                st.dataframe(df, use_container_width=True)
                st.caption(f"Mostrando 10 registros mais recentes de {len(pd.read_sql_query('SELECT COUNT(*) FROM irrigation_data', sqlite3.connect(db_path)))} total")
                
            except Exception as e:
                st.error(f"Erro ao carregar dados: {e}")
        else:
            st.warning("Banco de dados não encontrado. Execute a Fase 4 primeiro.")
    
    else:
        # Interface de chat
        st.subheader("💬 Chat com seus Dados")
        
        # Inicializa histórico de mensagens
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Mostra histórico de mensagens
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Faça uma pergunta sobre os dados agrícolas..."):
            # Adiciona mensagem do usuário ao histórico
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Mostra mensagem do usuário
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Processa resposta
            with st.chat_message("assistant"):
                with st.spinner("Analisando dados..."):
                    try:
                        # Carrega dados do banco
                        db_path = Path("fase_4_dashboard_ml/irrigation.db")
                        
                        if not db_path.exists():
                            response = "❌ Banco de dados não encontrado. Execute a Fase 4 primeiro para gerar dados."
                        else:
                            conn = sqlite3.connect(db_path)
                            df = pd.read_sql_query("SELECT * FROM irrigation_data ORDER BY id DESC LIMIT 50", conn)
                            conn.close()
                            
                            # Prepara contexto dos dados
                            stats = {
                                "total_registros": len(df),
                                "umidade_media": df['humidity'].mean(),
                                "umidade_min": df['humidity'].min(),
                                "umidade_max": df['humidity'].max(),
                                "ph_medio": df['ph'].mean(),
                                "ph_min": df['ph'].min(),
                                "ph_max": df['ph'].max(),
                                "fosforo_medio": df['phosphorus'].mean(),
                                "potassio_medio": df['potassium'].mean(),
                                "precisa_irrigacao": df['needs_irrigation'].sum(),
                                "nao_precisa_irrigacao": (df['needs_irrigation'] == 0).sum()
                            }
                            
                            # Amostra de dados recentes
                            sample_data = df.head(10).to_dict('records')
                            
                            # Monta prompt para a LLM
                            system_prompt = f"""Você é um assistente especializado em agricultura de precisão. 
                            Analise os dados de sensores agrícolas e responda perguntas de forma clara e objetiva.
                            
                            ESTATÍSTICAS DOS DADOS (últimos 50 registros):
                            - Total de sensores: {stats['total_registros']}
                            - Umidade do solo: média {stats['umidade_media']:.1f}%, mín {stats['umidade_min']:.1f}%, máx {stats['umidade_max']:.1f}%
                            - pH do solo: média {stats['ph_medio']:.1f}, mín {stats['ph_min']:.1f}, máx {stats['ph_max']:.1f}
                            - Fósforo: média {stats['fosforo_medio']:.1f} ppm
                            - Potássio: média {stats['potassio_medio']:.1f} ppm
                            - Sensores que precisam irrigação: {stats['precisa_irrigacao']}
                            - Sensores que NÃO precisam irrigação: {stats['nao_precisa_irrigacao']}
                            
                            AMOSTRA DOS 10 REGISTROS MAIS RECENTES:
                            {sample_data}
                            
                            Responda de forma técnica mas acessível, incluindo números e recomendações práticas quando relevante.
                            """
                            
                            # Chama API da OpenAI
                            import requests
                            import json
                            
                            headers = {
                                "Content-Type": "application/json",
                                "Authorization": f"Bearer {api_key}"
                            }
                            
                            payload = {
                                "model": model_choice,
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": 0.7,
                                "max_tokens": 800
                            }
                            
                            api_response = requests.post(
                                "https://api.openai.com/v1/chat/completions",
                                headers=headers,
                                json=payload,
                                timeout=30
                            )
                            
                            if api_response.status_code == 200:
                                result = api_response.json()
                                response = result['choices'][0]['message']['content']
                            else:
                                response = f"❌ Erro na API: {api_response.status_code} - {api_response.text}"
                    
                    except Exception as e:
                        response = f"❌ Erro ao processar pergunta: {str(e)}"
                    
                    # Mostra resposta
                    st.markdown(response)
                    
                    # Adiciona resposta ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Botão para limpar histórico
        if st.session_state.messages:
            if st.button("🗑️ Limpar Conversa"):
                st.session_state.messages = []
                st.rerun()
        
        # Sugestões de perguntas
        with st.expander("💡 Sugestões de Perguntas"):
            st.markdown("""
            - "Quantos sensores indicam necessidade de irrigação?"
            - "Qual é a umidade média do solo?"
            - "Existem áreas com pH fora da faixa ideal (6.0-7.5)?"
            - "Qual sensor tem o menor nível de fósforo?"
            - "Faça um resumo da situação geral das plantações"
            - "Quais são os 3 principais problemas identificados?"
            - "O nível de potássio está adequado?"
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>FarmTech Solutions v1.0</strong></p>
    <p>Sistema Integrado de Agricultura de Precisão com IA</p>
</div>
""", unsafe_allow_html=True)

#!/bin/bash

# ============================================
# FarmTech Solutions - Setup Script
# ============================================
# Este script automatiza a configuração inicial do projeto

echo "============================================"
echo "🌾 FarmTech Solutions - Setup Automático"
echo "============================================"
echo ""

# Verificar Python
echo "📋 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
else
    echo "❌ Python 3 não encontrado!"
    echo "💡 Instale Python 3.10+ em: https://www.python.org/downloads/"
    exit 1
fi

echo ""

# Verificar pip
echo "📋 Verificando pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✅ pip encontrado: $PIP_VERSION"
else
    echo "❌ pip não encontrado!"
    exit 1
fi

echo ""

# Criar ambiente virtual (opcional)
read -p "🤔 Deseja criar um ambiente virtual? (recomendado) [S/n]: " CREATE_VENV
CREATE_VENV=${CREATE_VENV:-S}

if [[ $CREATE_VENV =~ ^[Ss]$ ]]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    
    echo "✅ Ambiente virtual criado!"
    echo "💡 Para ativar:"
    echo "   Linux/Mac: source venv/bin/activate"
    echo "   Windows: venv\\Scripts\\activate"
    echo ""
    
    # Ativar ambiente virtual
    if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
        echo "✅ Ambiente virtual ativado"
    fi
fi

echo ""

# Instalar dependências
echo "📥 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo ""

# Verificar arquivos necessários
echo "📋 Verificando arquivos do projeto..."

FILES_TO_CHECK=(
    "app_integrated.py"
    "fase_4_dashboard_ml/scripts/genetic_optimizer.py"
    "fase_4_dashboard_ml/scripts/aws_manager.py"
    "fase_1_R_analysis/data/agro_data.csv"
)

MISSING_FILES=0

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "⚠️  $file não encontrado"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo ""

# Verificar modelo ML
if [ -f "fase_4_dashboard_ml/irrigation_model.joblib" ]; then
    echo "✅ Modelo ML encontrado"
else
    echo "⚠️  Modelo ML não encontrado"
    echo "💡 Execute: cd fase_4_dashboard_ml/scripts && python train_model.py"
fi

# Verificar modelo YOLO
if [ -f "fase_6_vision_yolo/best.pt" ]; then
    echo "✅ Modelo YOLO encontrado"
else
    echo "⚠️  Modelo YOLO não encontrado"
    echo "💡 Treine o modelo YOLO usando o notebook da Fase 6"
fi

echo ""

# Configurar AWS (opcional)
read -p "🤔 Deseja configurar credenciais AWS? [s/N]: " SETUP_AWS
SETUP_AWS=${SETUP_AWS:-N}

if [[ $SETUP_AWS =~ ^[Ss]$ ]]; then
    echo ""
    echo "🔑 Configuração AWS"
    read -p "AWS Access Key ID: " AWS_KEY
    read -p "AWS Secret Access Key: " AWS_SECRET
    read -p "AWS Region (padrão: us-east-1): " AWS_REGION
    AWS_REGION=${AWS_REGION:-us-east-1}
    
    export AWS_ACCESS_KEY_ID=$AWS_KEY
    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET
    export AWS_DEFAULT_REGION=$AWS_REGION
    
    echo "✅ Variáveis AWS configuradas (apenas para esta sessão)"
    echo "💡 Para tornar permanente, adicione ao ~/.bashrc ou ~/.zshrc"
else
    echo "ℹ️  Modo simulação será usado (sem credenciais AWS)"
fi

echo ""
echo "============================================"
echo "✅ Setup Concluído!"
echo "============================================"
echo ""
echo "🚀 Para executar o dashboard:"
echo "   streamlit run app_integrated.py"
echo ""
echo "📚 Documentação completa:"
echo "   - README_INTEGRATED.md"
echo "   - QUICKSTART.md"
echo ""
echo "💡 Acesse o dashboard em: http://localhost:8501"
echo ""
echo "🌾 FarmTech Solutions - Pronto para uso!"
echo "============================================"

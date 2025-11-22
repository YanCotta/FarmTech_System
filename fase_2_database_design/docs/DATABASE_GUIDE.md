# FarmTech Solutions - Guia do Sistema de Banco de Dados Enterprise

## 📚 Visão Geral

Este guia documenta o sistema de gerenciamento de banco de dados profissionalizado do **FarmTech Solutions**, utilizando **SQLAlchemy 2.0.23** (ORM) e **Alembic 1.13.1** (Migrations).

### ✨ Benefícios da Nova Arquitetura

- **Database-Agnostic**: Troque facilmente entre SQLite, PostgreSQL, MySQL sem alterar código
- **Versionamento de Schema**: Histórico completo de mudanças no banco via Alembic
- **Type-Safe**: Modelos ORM com tipagem forte e validação
- **Manutenibilidade**: Código mais limpo e organizado
- **Escalabilidade**: Pronto para migração para bancos enterprise (PostgreSQL/AWS RDS)

---

## 🏗️ Arquitetura

```
fase_2_database_design/
├── database_manager.py         # Modelos ORM + DatabaseManager
├── alembic.ini                 # Configuração do Alembic
├── migrations/                 # Migrações do banco
│   ├── env.py                  # Ambiente de migrações
│   ├── script.py.mako          # Template de migrations
│   └── versions/               # Histórico de versões
│       └── f8d6152866df_*.py   # Migration inicial
└── docs/
    └── DATABASE_GUIDE.md       # Este arquivo
```

---

## 📊 Modelos de Dados

### 1. IrrigationData
**Tabela**: `irrigation_data`

Armazena dados de sensores e decisão de irrigação (Fase 4 - Machine Learning).

| Campo            | Tipo      | Descrição                       |
|------------------|-----------|---------------------------------|
| `id`             | Integer   | PK, auto-increment              |
| `timestamp`      | DateTime  | Data/hora da medição            |
| `humidity`       | Float     | Umidade do solo (%)             |
| `ph`             | Float     | pH do solo                      |
| `phosphorus`     | Float     | Nível de fósforo (ppm)          |
| `potassium`      | Float     | Nível de potássio (ppm)         |
| `needs_irrigation` | Boolean | Necessita irrigação? (0/1)      |

**Uso no ML**: Target para modelo Random Forest de predição de irrigação.

---

### 2. SensorReading
**Tabela**: `sensor_readings`

Dados brutos dos sensores IoT ESP32 (Fase 3).

| Campo            | Tipo      | Descrição                       |
|------------------|-----------|---------------------------------|
| `id`             | Integer   | PK, auto-increment              |
| `timestamp`      | DateTime  | Data/hora da leitura            |
| `sensor_id`      | String(50)| ID do sensor ESP32              |
| `temperature`    | Float     | Temperatura (°C)                |
| `humidity`       | Float     | Umidade do ar (%)               |
| `soil_moisture`  | Float     | Umidade do solo (%)             |
| `light_level`    | Integer   | Nível de luz (lux)              |

**Integração**: Dados recebidos via MQTT/HTTP do ESP32.

---

### 3. PestDetection
**Tabela**: `pest_detections`

Detecções de pragas via YOLOv5 (Fase 6).

| Campo            | Tipo        | Descrição                       |
|------------------|-------------|---------------------------------|
| `id`             | Integer     | PK, auto-increment              |
| `timestamp`      | DateTime    | Data/hora da detecção           |
| `pest_type`      | String(100) | Tipo de praga detectada         |
| `confidence`     | Float       | Confiança da detecção (0-1)     |
| `location`       | String(200) | Localização GPS/Setor           |
| `image_path`     | String(500) | Caminho da imagem processada    |
| `alert_sent`     | Boolean     | Alerta AWS SNS enviado?         |

**Integração**: Alimentado por `app_integrated.py` módulo de Computer Vision.

---

## 🚀 Uso Básico

### Inicializar Banco de Dados

```python
from database_manager import initialize_database

# Cria banco, executa migrations e popula dados
db = initialize_database(seed=True)
```

### Consultas com ORM

```python
from database_manager import DatabaseManager, IrrigationData

db = DatabaseManager()
session = db.get_session()

try:
    # Buscar todos registros que precisam irrigação
    needs_water = session.query(IrrigationData).filter(
        IrrigationData.needs_irrigation == True
    ).all()
    
    for record in needs_water:
        print(f"Sensor {record.id}: Umidade {record.humidity}% - IRRIGAR!")
    
finally:
    session.close()
```

### Inserir Novos Dados

```python
from database_manager import DatabaseManager, IrrigationData
from datetime import datetime

db = DatabaseManager()
session = db.get_session()

try:
    new_reading = IrrigationData(
        humidity=25.5,
        ph=6.8,
        phosphorus=45.0,
        potassium=120.0,
        needs_irrigation=True
    )
    
    session.add(new_reading)
    session.commit()
    print(f"✅ Registro criado com ID: {new_reading.id}")
    
except Exception as e:
    session.rollback()
    print(f"❌ Erro: {e}")
finally:
    session.close()
```

---

## 🔄 Migrações com Alembic

### Comandos Essenciais

```bash
# Navegar para o diretório correto
cd fase_2_database_design/

# Criar nova migration (após alterar modelos)
alembic revision --autogenerate -m "Adicionar coluna temperatura"

# Aplicar migrations pendentes
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico de migrations
alembic history

# Ver status atual
alembic current
```

### Criar Nova Migration Manualmente

```python
# migrations/versions/XXXXX_adicionar_coluna.py

def upgrade():
    op.add_column('irrigation_data', 
                  sa.Column('temperature', sa.Float(), nullable=True))

def downgrade():
    op.drop_column('irrigation_data', 'temperature')
```

---

## 🔌 Trocar Banco de Dados

### SQLite (Desenvolvimento)
```python
db = DatabaseManager("sqlite:///irrigation.db")
```

### PostgreSQL (Produção)
```python
db = DatabaseManager("postgresql://user:password@localhost:5432/farmtech")
```

### MySQL
```python
db = DatabaseManager("mysql+pymysql://user:password@localhost/farmtech")
```

**Vantagem**: O código ORM permanece **idêntico** independente do banco!

---

## 🛠️ Manutenção

### Estatísticas do Banco

```python
db = DatabaseManager()
stats = db.get_statistics()

for table, count in stats.items():
    print(f"{table}: {count} registros")
```

### Limpar Todos os Dados (DEV ONLY!)

```python
db = DatabaseManager()
db.clear_all_data()  # ⚠️ USE COM CUIDADO!
```

### Backup do Banco SQLite

```bash
# Backup manual
cp irrigation.db irrigation_backup_$(date +%Y%m%d).db

# Usando sqlite3
sqlite3 irrigation.db ".backup 'backup.db'"
```

---

## 📈 Performance

### Otimizações Implementadas

1. **Batch Inserts**: Commits em lotes de 50 registros
2. **Connection Pooling**: Gerenciado automaticamente pelo SQLAlchemy
3. **Lazy Loading**: Relacionamentos carregados sob demanda
4. **Índices**: Aplicar nas colunas mais consultadas (futuro)

### Criar Índices (Exemplo)

```python
# Em nova migration
def upgrade():
    op.create_index('idx_timestamp', 'irrigation_data', ['timestamp'])
    op.create_index('idx_needs_irrigation', 'irrigation_data', ['needs_irrigation'])
```

---

## 🔐 Segurança

### Boas Práticas

1. **Nunca commitar `irrigation.db`** no Git (já em `.gitignore`)
2. **Usar variáveis de ambiente** para credenciais de produção
3. **Validar inputs** antes de inserir no banco
4. **SQL Injection**: Protegido automaticamente pelo SQLAlchemy ORM

### Exemplo com .env

```python
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL", "sqlite:///irrigation.db")
db = DatabaseManager(db_url)
```

---

## 🧪 Testes

### Testar Conexão

```python
python database_manager.py
```

### Testar Migrations

```bash
cd fase_2_database_design/

# Aplicar migrations
alembic upgrade head

# Verificar tabelas criadas
sqlite3 ../irrigation.db ".tables"
```

---

## 📚 Referências

- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/en/20/
- **Alembic Tutorial**: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Database Design**: `/fase_2_database_design/docs/README.md`

---

## 🎯 Roadmap

### Fase Atual (v2.0)
- ✅ SQLAlchemy ORM
- ✅ Alembic Migrations
- ✅ 3 Modelos (IrrigationData, SensorReading, PestDetection)
- ✅ Seeding automático

### Futuro (v2.1+)
- [ ] Adicionar índices para performance
- [ ] Implementar relationships entre modelos
- [ ] Migração para PostgreSQL (AWS RDS)
- [ ] Adicionar soft deletes (deleted_at)
- [ ] Audit trail (created_by, updated_at)

---

**Desenvolvido por**: FarmTech Engineering Team  
**Última atualização**: 22/11/2025  
**Versão**: 2.0.0 (Enterprise Edition)

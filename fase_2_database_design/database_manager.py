"""
Database Manager - FarmTech Solutions
======================================

Sistema de gerenciamento de banco de dados usando SQLAlchemy ORM e Alembic.
Este módulo profissionaliza a camada de dados, tornando o sistema agnóstico
de banco de dados (SQLite, PostgreSQL, MySQL, etc.).

Autor: FarmTech Engineering Team
Data: 2025-11-22
Versão: 2.0.0 (Enterprise Edition)
"""

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime
from pathlib import Path
import logging
import random
from typing import Optional, List

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base para modelos ORM
Base = declarative_base()


# ============================================
# DEFINIÇÃO DE MODELOS ORM
# ============================================

class IrrigationData(Base):
    """
    Modelo ORM para dados de irrigação.
    
    Representa medições de sensores e decisão de irrigação.
    """
    __tablename__ = 'irrigation_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    
    # Dados dos sensores
    humidity = Column(Float, nullable=False, comment="Umidade do solo (%)")
    ph = Column(Float, nullable=False, comment="pH do solo")
    phosphorus = Column(Float, nullable=False, comment="Nível de fósforo (ppm)")
    potassium = Column(Float, nullable=False, comment="Nível de potássio (ppm)")
    
    # Decisão de irrigação (target)
    needs_irrigation = Column(Boolean, nullable=False, comment="Necessita irrigação? (0=Não, 1=Sim)")
    
    def __repr__(self):
        return (f"<IrrigationData(id={self.id}, humidity={self.humidity}, "
                f"needs_irrigation={self.needs_irrigation})>")


class SensorReading(Base):
    """
    Modelo ORM para leituras de sensores IoT (Fase 3).
    
    Armazena dados brutos dos sensores ESP32.
    """
    __tablename__ = 'sensor_readings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    sensor_id = Column(String(50), nullable=False, comment="ID do sensor ESP32")
    
    # Leituras
    temperature = Column(Float, comment="Temperatura (°C)")
    humidity = Column(Float, comment="Umidade relativa do ar (%)")
    soil_moisture = Column(Float, comment="Umidade do solo (%)")
    light_level = Column(Integer, comment="Nível de luz (lux)")
    
    def __repr__(self):
        return f"<SensorReading(id={self.id}, sensor_id={self.sensor_id}, temp={self.temperature}°C)>"


class PestDetection(Base):
    """
    Modelo ORM para detecções de pragas (Fase 6).
    
    Armazena resultados do modelo YOLO.
    """
    __tablename__ = 'pest_detections'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    
    # Informações da detecção
    pest_type = Column(String(100), nullable=False, comment="Tipo de praga detectada")
    confidence = Column(Float, nullable=False, comment="Confiança da detecção (0-1)")
    location = Column(String(200), comment="Localização da detecção")
    image_path = Column(String(500), comment="Caminho da imagem")
    
    # Ação tomada
    alert_sent = Column(Boolean, default=False, comment="Alerta AWS enviado?")
    
    def __repr__(self):
        return f"<PestDetection(id={self.id}, pest={self.pest_type}, confidence={self.confidence:.2%})>"


# ============================================
# DATABASE MANAGER CLASS
# ============================================

class DatabaseManager:
    """
    Gerenciador de banco de dados enterprise-grade.
    
    Responsabilidades:
    - Criar conexão com banco de dados
    - Executar migrações (criar tabelas)
    - Popular dados iniciais (seeding)
    - Fornecer sessões para operações CRUD
    
    Exemplo:
        >>> db_manager = DatabaseManager()
        >>> db_manager.run_migrations()
        >>> db_manager.seed_data()
        >>> 
        >>> session = db_manager.get_session()
        >>> data = session.query(IrrigationData).all()
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            database_url: URL de conexão (ex: 'sqlite:///irrigation.db' ou 
                         'postgresql://user:pass@localhost/farmtech')
                         Se None, usa SQLite no diretório fase_4_dashboard_ml
        """
        if database_url is None:
            # Default: SQLite na pasta fase_4_dashboard_ml
            db_path = Path(__file__).parent.parent / "irrigation.db"
            database_url = f"sqlite:///{db_path}"
        
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info(f"DatabaseManager inicializado: {database_url}")
    
    def run_migrations(self) -> None:
        """
        Executa migrações do banco de dados (cria todas as tabelas).
        
        Em produção, isso seria substituído por `alembic upgrade head`.
        """
        logger.info("Executando migrações do banco de dados...")
        
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("✅ Migrações concluídas com sucesso!")
            
            # Lista tabelas criadas
            tables = Base.metadata.tables.keys()
            logger.info(f"Tabelas disponíveis: {', '.join(tables)}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar migrações: {e}")
            raise
    
    def get_session(self) -> Session:
        """
        Retorna uma nova sessão do banco de dados.
        
        Returns:
            Session: Sessão SQLAlchemy para operações CRUD
        
        Exemplo:
            >>> session = db_manager.get_session()
            >>> try:
            ...     data = session.query(IrrigationData).all()
            ...     session.commit()
            ... finally:
            ...     session.close()
        """
        return self.SessionLocal()
    
    def seed_data(self, num_records: int = 200) -> None:
        """
        Popula o banco com dados sintéticos iniciais (seeding).
        
        Insere dados apenas se a tabela estiver vazia (idempotente).
        
        Args:
            num_records: Número de registros a serem criados
        """
        session = self.get_session()
        
        try:
            # Verifica se já existe dados
            existing_count = session.query(IrrigationData).count()
            
            if existing_count > 0:
                logger.info(f"⚠️ Tabela já contém {existing_count} registros. Pulando seed.")
                return
            
            logger.info(f"Gerando {num_records} registros sintéticos...")
            
            records = []
            for i in range(num_records):
                # Gera dados sintéticos baseados em lógica agrícola
                humidity = random.uniform(15, 60)
                ph = random.uniform(5.5, 8.5)
                phosphorus = random.uniform(10, 100)
                potassium = random.uniform(50, 300)
                
                # Lógica de decisão: irriga se umidade < 30% OU pH fora da faixa ideal
                needs_irrigation = (humidity < 30) or (ph < 6.0) or (ph > 7.5)
                
                record = IrrigationData(
                    humidity=round(humidity, 2),
                    ph=round(ph, 2),
                    phosphorus=round(phosphorus, 2),
                    potassium=round(potassium, 2),
                    needs_irrigation=needs_irrigation
                )
                records.append(record)
                
                # Commit em lotes de 50 para performance
                if (i + 1) % 50 == 0:
                    session.add_all(records)
                    session.commit()
                    records = []
                    logger.info(f"Inseridos {i + 1} registros...")
            
            # Insere registros restantes
            if records:
                session.add_all(records)
                session.commit()
            
            final_count = session.query(IrrigationData).count()
            logger.info(f"✅ Seed concluído! Total de registros: {final_count}")
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao popular dados: {e}")
            raise
        finally:
            session.close()
    
    def get_statistics(self) -> dict:
        """
        Retorna estatísticas do banco de dados.
        
        Returns:
            dict: Estatísticas de cada tabela
        """
        session = self.get_session()
        
        try:
            stats = {
                'irrigation_data': session.query(IrrigationData).count(),
                'sensor_readings': session.query(SensorReading).count(),
                'pest_detections': session.query(PestDetection).count(),
            }
            return stats
        finally:
            session.close()
    
    def clear_all_data(self) -> None:
        """
        Remove todos os dados das tabelas (use com cuidado!).
        
        Útil para testes e desenvolvimento.
        """
        session = self.get_session()
        
        try:
            logger.warning("⚠️ ATENÇÃO: Removendo todos os dados...")
            
            session.query(PestDetection).delete()
            session.query(SensorReading).delete()
            session.query(IrrigationData).delete()
            
            session.commit()
            logger.info("✅ Todos os dados foram removidos")
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Erro ao limpar dados: {e}")
            raise
        finally:
            session.close()


# ============================================
# FUNÇÕES DE CONVENIÊNCIA
# ============================================

def initialize_database(database_url: Optional[str] = None, seed: bool = True) -> DatabaseManager:
    """
    Inicializa o banco de dados completo (migrations + seed).
    
    Args:
        database_url: URL do banco de dados
        seed: Se True, popula dados iniciais
    
    Returns:
        DatabaseManager: Instância do gerenciador
    
    Exemplo:
        >>> db = initialize_database()
        >>> session = db.get_session()
    """
    db_manager = DatabaseManager(database_url)
    db_manager.run_migrations()
    
    if seed:
        db_manager.seed_data()
    
    return db_manager


# ============================================
# SCRIPT PRINCIPAL (para execução standalone)
# ============================================

if __name__ == "__main__":
    """
    Execução standalone para setup inicial do banco.
    
    Uso:
        python database_manager.py
    """
    print("=" * 70)
    print("FarmTech Solutions - Database Manager (Enterprise Edition)")
    print("=" * 70)
    print()
    
    # Inicializa banco de dados
    db = initialize_database(seed=True)
    
    # Mostra estatísticas
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS DO BANCO DE DADOS")
    print("=" * 70)
    stats = db.get_statistics()
    for table, count in stats.items():
        print(f"  {table:.<50} {count:>5} registros")
    
    print("\n" + "=" * 70)
    print("✅ Banco de dados pronto para uso!")
    print("=" * 70)
    
    # Exemplo de query
    print("\n📊 Exemplo de consulta - Primeiros 5 registros:")
    print("-" * 70)
    
    session = db.get_session()
    try:
        records = session.query(IrrigationData).limit(5).all()
        for record in records:
            status = "🚰 IRRIGAR" if record.needs_irrigation else "✅ OK"
            print(f"  {record.id:>3} | Umidade: {record.humidity:>5.1f}% | pH: {record.ph:.1f} | {status}")
    finally:
        session.close()
    
    print()

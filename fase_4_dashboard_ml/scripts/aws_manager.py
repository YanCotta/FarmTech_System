"""
AWS Manager - Gerenciador de Serviços AWS para FarmTech Solutions
===================================================================

Este módulo fornece integração com serviços AWS, especialmente SNS para alertas.
Implementa fallback de simulação quando credenciais AWS não estão disponíveis.

Baseado no desafio "Ir Além 1" - Integração AWS

Classes:
    - AWSAlertManager: Classe principal (nova, mais robusta)
    - AWSManager: Classe legada (mantida para compatibilidade)

Autor: FIAP IA Engineering Team - Fase 7 Integration
Data: 2025-11-21
Versão: 2.0.0
"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Níveis de severidade do alerta"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


class AlertType(Enum):
    """Tipos de alertas suportados"""
    HUMIDITY = "HUMIDITY"
    SOIL_MOISTURE = "SOIL_MOISTURE"
    PEST_DETECTION = "PEST_DETECTION"
    TEMPERATURE = "TEMPERATURE"
    SYSTEM = "SYSTEM"
    CUSTOM = "CUSTOM"


# ============================================
# CLASSE PRINCIPAL (NOVA - MAIS ROBUSTA)
# ============================================

class AWSAlertManager:
    """
    Gerenciador de Alertas AWS SNS com Fallback Automático (Versão 2.0).
    
    Esta classe implementa o desafio "Ir Além 1" com tratamento robusto de exceções.
    Se as credenciais AWS não estiverem configuradas ou houver falha na conexão,
    o sistema automaticamente entra em MODO SIMULAÇÃO, garantindo que a aplicação
    nunca quebre por falta de configuração AWS.
    
    **REGRA CRÍTICA:** Este código NUNCA quebra a aplicação, mesmo sem AWS configurado.
    
    Attributes:
        simulation_mode (bool): True se estiver em modo simulação (sem AWS real)
        sns_client: Cliente boto3 SNS (None se em modo simulação)
        topic_arn (str): ARN do tópico SNS padrão
        region (str): Região AWS configurada
        
    Example:
        >>> manager = AWSAlertManager()
        >>> # Funciona mesmo sem AWS configurado!
        >>> manager.send_alert("Teste", "Mensagem de teste")
        >>> 
        >>> # Métodos específicos
        >>> manager.notify_low_humidity(25.5, threshold=30.0)
        >>> manager.notify_pest_detection("Lagarta", confidence=0.92)
    """
    
    def __init__(
        self,
        topic_arn: Optional[str] = None,
        region: str = 'us-east-1'
    ):
        """
        Inicializa o gerenciador de alertas AWS com fallback automático.
        
        Args:
            topic_arn: ARN do tópico SNS. Se None, usa variável de ambiente
                      AWS_SNS_TOPIC_ARN ou cria um padrão
            region: Região AWS (default: us-east-1)
        
        Note:
            Se as credenciais AWS não estiverem configuradas ou falharem,
            o sistema automaticamente entra em simulation_mode=True.
            A aplicação NUNCA quebra por falta de AWS.
        """
        self.simulation_mode = False
        self.sns_client = None
        self.region = region
        self.topic_arn = topic_arn or os.getenv(
            'AWS_SNS_TOPIC_ARN',
            f'arn:aws:sns:{region}:123456789012:FarmTechAlerts'
        )
        
        # Estatísticas
        self._alerts_sent = 0
        self._alerts_failed = 0
        
        # Tenta inicializar conexão AWS (com fallback automático)
        self._initialize_aws_connection()
    
    def _initialize_aws_connection(self) -> None:
        """
        Tenta estabelecer conexão com AWS SNS.
        
        Em caso de QUALQUER falha (credenciais ausentes, permissões, rede, etc.),
        ativa automaticamente o modo simulação SEM QUEBRAR A APLICAÇÃO.
        """
        try:
            import boto3
            from botocore.exceptions import (
                NoCredentialsError,
                PartialCredentialsError,
                ClientError,
                BotoCoreError
            )
            
            # Tenta criar o cliente SNS
            self.sns_client = boto3.client('sns', region_name=self.region)
            
            # Valida credenciais com uma chamada leve
            try:
                self.sns_client.list_topics(MaxResults=1)
                
                # Sucesso! Credenciais válidas
                self.simulation_mode = False
                logger.info(f"✅ AWS SNS conectado (região: {self.region})")
                logger.info(f"📡 Tópico: {self.topic_arn}")
                    
            except (NoCredentialsError, PartialCredentialsError) as e:
                # Credenciais não configuradas
                logger.warning("⚠️  Credenciais AWS não encontradas")
                self._activate_simulation_mode("Credenciais AWS ausentes")
                
            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                
                if error_code in ['InvalidClientTokenId', 'SignatureDoesNotMatch', 'AccessDenied']:
                    logger.warning(f"⚠️  Erro de autenticação AWS: {error_code}")
                    self._activate_simulation_mode(f"Autenticação falhou: {error_code}")
                else:
                    logger.warning(f"⚠️  Erro AWS: {error_code}")
                    self._activate_simulation_mode(f"Erro AWS: {e}")
                    
            except BotoCoreError as e:
                # Erros de rede, timeout, etc.
                logger.warning(f"⚠️  Erro de conexão: {e}")
                self._activate_simulation_mode(f"Erro de conexão: {e}")
                
        except ImportError:
            # boto3 não instalado
            logger.error("❌ boto3 não instalado! Execute: pip install boto3")
            self._activate_simulation_mode("boto3 não instalado")
            
        except Exception as e:
            # Qualquer outro erro inesperado - NUNCA quebra
            logger.error(f"❌ Erro inesperado: {e}")
            self._activate_simulation_mode(f"Erro inesperado: {e}")
    
    def _activate_simulation_mode(self, reason: str) -> None:
        """Ativa o modo simulação (fallback seguro)."""
        self.simulation_mode = True
        self.sns_client = None
        logger.warning("🔧 MODO SIMULAÇÃO ATIVADO")
        logger.warning(f"   Motivo: {reason}")
        logger.warning("   Alertas serão logados localmente")
    
    def send_alert(
        self,
        subject: str,
        message: str,
        alert_type: AlertType = AlertType.CUSTOM,
        severity: AlertLevel = AlertLevel.INFO
    ) -> Dict[str, Any]:
        """
        Envia um alerta (real via SNS ou simulado).
        
        **GARANTE:** Este método NUNCA gera exceção. Sempre retorna um resultado.
        
        Args:
            subject: Assunto do alerta
            message: Mensagem do alerta
            alert_type: Tipo do alerta (enum AlertType)
            severity: Severidade do alerta (enum AlertLevel)
        
        Returns:
            Dict com resultado:
                {
                    'success': bool,
                    'mode': 'real' ou 'simulation',
                    'message_id': str (se real) ou None,
                    'timestamp': str
                }
        """
        timestamp = datetime.now().isoformat()
        full_subject = f"[{severity.value}] {subject}"
        full_message = f"[{alert_type.value}] {message}"
        
        # MODO SIMULAÇÃO
        if self.simulation_mode:
            return self._simulate_alert(full_subject, full_message, timestamp, severity)
        
        # MODO REAL (AWS SNS)
        return self._send_real_alert(full_subject, full_message, timestamp)
    
    def _simulate_alert(
        self,
        subject: str,
        message: str,
        timestamp: str,
        severity: AlertLevel
    ) -> Dict[str, Any]:
        """Simula o envio de um alerta (modo sem AWS)."""
        # Emoji baseado na severidade
        severity_icons = {
            AlertLevel.INFO: "ℹ️",
            AlertLevel.WARNING: "⚠️",
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.EMERGENCY: "🚨"
        }
        icon = severity_icons.get(severity, "📢")
        
        # Log formatado
        print("\n" + "=" * 70)
        print(f"{icon}  [AWS SNS SIMULATION MODE]")
        print("=" * 70)
        print(f"Subject: {subject}")
        print(f"Topic: {self.topic_arn}")
        print(f"Time: {timestamp}")
        print("-" * 70)
        print(message)
        print("=" * 70)
        print("✅ Alerta simulado (AWS não configurado)")
        print("=" * 70 + "\n")
        
        self._alerts_sent += 1
        
        return {
            'success': True,
            'mode': 'simulation',
            'message_id': None,
            'timestamp': timestamp,
            'simulated': True
        }
    
    def _send_real_alert(
        self,
        subject: str,
        message: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """Envia alerta real via AWS SNS."""
        try:
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Subject=subject[:100],  # SNS limita a 100 chars
                Message=message
            )
            
            message_id = response.get('MessageId')
            self._alerts_sent += 1
            
            logger.info(f"✅ Alerta enviado via AWS SNS")
            logger.info(f"   Message ID: {message_id}")
            
            return {
                'success': True,
                'mode': 'real',
                'message_id': message_id,
                'timestamp': timestamp
            }
            
        except Exception as e:
            self._alerts_failed += 1
            logger.error(f"❌ Erro ao enviar via SNS: {e}")
            
            # Fallback para simulação
            logger.warning("🔄 Fazendo fallback para modo simulação...")
            return self._simulate_alert(subject, message, timestamp, AlertLevel.WARNING)
    
    # ========================================
    # MÉTODOS ESPECÍFICOS (CASOS DE USO)
    # ========================================
    
    def notify_low_humidity(
        self,
        humidity_value: float,
        threshold: float = 30.0,
        location: str = "Sensor Principal"
    ) -> Dict[str, Any]:
        """
        Envia alerta de umidade do solo crítica (Fase 3 - IoT).
        
        Args:
            humidity_value: Valor atual da umidade (%)
            threshold: Limite mínimo aceitável (%)
            location: Localização do sensor
        
        Returns:
            Dict com resultado do envio
        
        Example:
            >>> manager.notify_low_humidity(22.5, threshold=30.0)
        """
        diff = threshold - humidity_value
        
        # Determina severidade
        if diff >= 20:
            severity = AlertLevel.EMERGENCY
        elif diff >= 10:
            severity = AlertLevel.CRITICAL
        else:
            severity = AlertLevel.WARNING
        
        subject = f"Umidade Crítica: {humidity_value:.1f}%"
        message = (
            f"⚠️ UMIDADE DO SOLO CRÍTICA!\n\n"
            f"Umidade atual: {humidity_value:.1f}%\n"
            f"Limite mínimo: {threshold:.1f}%\n"
            f"Déficit: {diff:.1f}%\n"
            f"Localização: {location}\n\n"
            f"AÇÃO: Ativar irrigação imediatamente!"
        )
        
        return self.send_alert(
            subject=subject,
            message=message,
            alert_type=AlertType.SOIL_MOISTURE,
            severity=severity
        )
    
    def notify_pest_detection(
        self,
        pest_name: str,
        confidence: float,
        image_path: Optional[str] = None,
        location: str = "Área Monitorada"
    ) -> Dict[str, Any]:
        """
        Envia alerta de detecção de praga via YOLO (Fase 6).
        
        Args:
            pest_name: Nome da praga detectada
            confidence: Confiança da detecção (0.0 a 1.0)
            image_path: Caminho da imagem (opcional)
            location: Localização da detecção
        
        Returns:
            Dict com resultado do envio
        
        Example:
            >>> manager.notify_pest_detection("Lagarta", confidence=0.94)
        """
        confidence_pct = confidence * 100
        
        # Severidade baseada na confiança
        if confidence >= 0.90:
            severity = AlertLevel.CRITICAL
        elif confidence >= 0.70:
            severity = AlertLevel.WARNING
        else:
            severity = AlertLevel.INFO
        
        subject = f"Praga Detectada: {pest_name}"
        message = (
            f"🐛 PRAGA DETECTADA!\n\n"
            f"Praga: {pest_name}\n"
            f"Confiança: {confidence_pct:.1f}%\n"
            f"Localização: {location}\n"
        )
        
        if image_path:
            message += f"Imagem: {image_path}\n"
        
        message += "\nAÇÃO: Inspecionar área e avaliar controle."
        
        return self.send_alert(
            subject=subject,
            message=message,
            alert_type=AlertType.PEST_DETECTION,
            severity=severity
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de alertas."""
        total = self._alerts_sent + self._alerts_failed
        success_rate = (self._alerts_sent / total * 100) if total > 0 else 0
        
        return {
            'total_sent': self._alerts_sent,
            'total_failed': self._alerts_failed,
            'success_rate': success_rate,
            'simulation_mode': self.simulation_mode
        }
    
    def __repr__(self) -> str:
        mode = "SIMULATION" if self.simulation_mode else "AWS REAL"
        return f"AWSAlertManager(mode={mode}, alerts={self._alerts_sent})"


# ============================================
# CLASSE LEGADA (MANTIDA PARA COMPATIBILIDADE)
# ============================================

class AWSManager:
    """
    **[CLASSE LEGADA - Use AWSAlertManager para novos projetos]**
    
    Gerenciador de serviços AWS para o sistema FarmTech (v1.0).
    
    Mantida para compatibilidade com código existente.
    Para novos projetos, use AWSAlertManager que possui tratamento
    de exceções mais robusto.
    
    Attributes:
        region_name (str): Região AWS a ser usada
        simulate_mode (bool): Se True, sempre simula (útil para testes)
        sns_client: Cliente boto3 SNS (None se não disponível)
    """
    
    def __init__(self, region_name: str = 'us-east-1', simulate_mode: bool = False):
        """
        Inicializa o gerenciador AWS.
        
        Args:
            region_name: Região AWS (padrão: us-east-1)
            simulate_mode: Força modo simulação mesmo se credenciais disponíveis
        """
        self.region_name = region_name
        self.simulate_mode = simulate_mode
        self.sns_client = None
        
        # Tenta inicializar cliente SNS
        if not simulate_mode:
            self._initialize_sns_client()
    
    def _initialize_sns_client(self) -> bool:
        """
        Inicializa o cliente SNS do boto3.
        
        Returns:
            True se inicializado com sucesso, False caso contrário
        """
        # Tenta importar boto3 primeiro
        try:
            import boto3
            from botocore.exceptions import NoCredentialsError, PartialCredentialsError
        except ImportError:
            logger.warning("⚠️  Biblioteca boto3 não instalada")
            logger.info("💡 Execute: pip install boto3")
            logger.info("🔄 Modo simulação será ativado")
            self.sns_client = None
            return False
        
        # Se chegou aqui, boto3 está instalado
        try:
            # Tenta criar cliente SNS
            self.sns_client = boto3.client('sns', region_name=self.region_name)
            
            # Testa as credenciais fazendo uma chamada simples
            self.sns_client.list_topics(MaxResults=1)
            
            logger.info(f"✅ Cliente AWS SNS inicializado com sucesso na região {self.region_name}")
            return True
            
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.warning(f"⚠️  Credenciais AWS não encontradas: {e}")
            logger.info("🔄 Modo simulação será ativado")
            self.sns_client = None
            return False
            
        except Exception as e:
            logger.warning(f"⚠️  Erro ao inicializar cliente AWS: {e}")
            logger.info("🔄 Modo simulação será ativado")
            self.sns_client = None
            return False
    
    def send_alert_sns(
        self,
        message: str,
        subject: str = "Alerta FarmTech Solutions",
        topic_arn: str = "arn:aws:sns:us-east-1:123456789:FarmAlerts",
        level: AlertLevel = AlertLevel.INFO
    ) -> Dict[str, Any]:
        """
        Envia alerta via AWS SNS ou simula o envio.
        
        Args:
            message: Mensagem do alerta
            subject: Assunto da notificação
            topic_arn: ARN do tópico SNS
            level: Nível de severidade do alerta
            
        Returns:
            Dicionário com resultado do envio contendo:
                - success (bool): Se o envio foi bem-sucedido
                - simulated (bool): Se foi simulado
                - message_id (str): ID da mensagem (se real)
                - timestamp (str): Timestamp do envio
                - details (str): Detalhes adicionais
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Adiciona nível de severidade à mensagem
        formatted_message = f"[{level.value}] {message}"
        
        # Se cliente SNS disponível e não em modo simulação
        if self.sns_client is not None and not self.simulate_mode:
            try:
                response = self.sns_client.publish(
                    TopicArn=topic_arn,
                    Subject=subject,
                    Message=formatted_message
                )
                
                message_id = response.get('MessageId', 'unknown')
                logger.info(f"✅ Alerta AWS SNS enviado com sucesso! MessageId: {message_id}")
                
                return {
                    'success': True,
                    'simulated': False,
                    'message_id': message_id,
                    'timestamp': timestamp,
                    'level': level.value,
                    'details': f"Alerta enviado para {topic_arn}"
                }
                
            except Exception as e:
                logger.error(f"❌ Erro ao enviar alerta SNS: {e}")
                logger.info("🔄 Tentando modo simulação...")
                # Fallback para simulação
                return self._simulate_alert_send(formatted_message, subject, topic_arn, level, timestamp)
        
        else:
            # Modo simulação
            return self._simulate_alert_send(formatted_message, subject, topic_arn, level, timestamp)
    
    def _simulate_alert_send(
        self,
        message: str,
        subject: str,
        topic_arn: str,
        level: AlertLevel,
        timestamp: str
    ) -> Dict[str, Any]:
        """
        Simula o envio de um alerta AWS SNS.
        
        Args:
            message: Mensagem do alerta
            subject: Assunto
            topic_arn: ARN do tópico
            level: Nível de severidade
            timestamp: Timestamp
            
        Returns:
            Dicionário com resultado simulado
        """
        # Gera ID simulado
        import hashlib
        message_id = hashlib.md5(f"{message}{timestamp}".encode()).hexdigest()[:16]
        
        # Log formatado e estilizado
        print("\n" + "=" * 70)
        print("🔔 [SIMULAÇÃO AWS SNS] ALERTA ENVIADO")
        print("=" * 70)
        print(f"📅 Timestamp:    {timestamp}")
        print(f"🎯 Tópico ARN:   {topic_arn}")
        print(f"📋 Assunto:      {subject}")
        print(f"⚠️  Nível:        {level.value}")
        print(f"🆔 Message ID:   sim-{message_id}")
        print("-" * 70)
        print(f"💬 Mensagem:")
        print(f"   {message}")
        print("=" * 70 + "\n")
        
        logger.info(f"🔄 [SIMULAÇÃO] Alerta enviado: {message[:50]}...")
        
        return {
            'success': True,
            'simulated': True,
            'message_id': f"sim-{message_id}",
            'timestamp': timestamp,
            'level': level.value,
            'details': "Alerta simulado - AWS não configurado"
        }
    
    def send_soil_moisture_alert(self, humidity: float, threshold: float = 30.0) -> Dict[str, Any]:
        """
        Envia alerta específico sobre umidade do solo baixa.
        
        Args:
            humidity: Valor atual de umidade
            threshold: Limite mínimo de umidade
            
        Returns:
            Resultado do envio do alerta
        """
        if humidity < threshold:
            level = AlertLevel.WARNING if humidity > threshold * 0.5 else AlertLevel.CRITICAL
            message = (
                f"⚠️ ALERTA DE UMIDADE DO SOLO\n\n"
                f"Umidade atual: {humidity:.1f}%\n"
                f"Limite mínimo: {threshold:.1f}%\n"
                f"Déficit: {threshold - humidity:.1f}%\n\n"
                f"Ação recomendada: Verificar sistema de irrigação e ativar bomba se necessário."
            )
            
            return self.send_alert_sns(
                message=message,
                subject="⚠️ Alerta: Umidade do Solo Baixa",
                level=level
            )
        
        return {
            'success': True,
            'simulated': False,
            'details': 'Umidade dentro do limite, nenhum alerta necessário'
        }
    
    def send_pest_detection_alert(
        self,
        pest_type: str,
        confidence: float,
        location: str = "Área monitorada"
    ) -> Dict[str, Any]:
        """
        Envia alerta sobre detecção de praga via YOLO.
        
        Args:
            pest_type: Tipo de praga detectada
            confidence: Confiança da detecção (0-100)
            location: Localização da detecção
            
        Returns:
            Resultado do envio do alerta
        """
        level = AlertLevel.WARNING if confidence > 70 else AlertLevel.INFO
        
        message = (
            f"🐛 ALERTA DE DETECÇÃO DE PRAGA\n\n"
            f"Tipo detectado: {pest_type}\n"
            f"Confiança: {confidence:.1f}%\n"
            f"Localização: {location}\n\n"
            f"Ação recomendada: Inspecionar área e avaliar necessidade de controle."
        )
        
        return self.send_alert_sns(
            message=message,
            subject=f"🐛 Alerta: Praga Detectada - {pest_type}",
            level=level
        )
    
    def send_system_alert(
        self,
        alert_type: str,
        details: str,
        level: AlertLevel = AlertLevel.INFO
    ) -> Dict[str, Any]:
        """
        Envia alerta genérico do sistema.
        
        Args:
            alert_type: Tipo de alerta
            details: Detalhes do alerta
            level: Nível de severidade
            
        Returns:
            Resultado do envio do alerta
        """
        message = (
            f"🔔 ALERTA DO SISTEMA FARMTECH\n\n"
            f"Tipo: {alert_type}\n"
            f"Detalhes: {details}\n"
        )
        
        return self.send_alert_sns(
            message=message,
            subject=f"FarmTech: {alert_type}",
            level=level
        )
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status da conexão AWS.
        
        Returns:
            Dicionário com informações de status
        """
        return {
            'aws_configured': self.sns_client is not None,
            'simulate_mode': self.simulate_mode or self.sns_client is None,
            'region': self.region_name,
            'service': 'SNS'
        }


# ============================================
# EXEMPLOS DE USO
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" " * 15 + "AWS Alert Manager - Sistema de Alertas")
    print(" " * 20 + "FarmTech Solutions - Fase 7")
    print("=" * 70)
    
    # ========================================
    # EXEMPLO 1: Usar a nova classe (recomendado)
    # ========================================
    print("\n📋 EXEMPLO 1: Usando AWSAlertManager (Nova Versão)")
    print("-" * 70)
    
    manager = AWSAlertManager()
    
    # Mostra status
    print(f"\n🔧 Status: {manager}")
    print(f"   Modo Simulação: {'SIM ⚠️' if manager.simulation_mode else 'NÃO ✅'}")
    
    # Teste 1: Alerta de umidade
    print("\n🧪 Teste 1: Alerta de Umidade Crítica (Fase 3 - IoT)")
    result1 = manager.notify_low_humidity(
        humidity_value=22.5,
        threshold=30.0,
        location="Setor A - Plantação de Soja"
    )
    print(f"   ✅ Resultado: {result1['success']} | Modo: {result1['mode']}")
    
    # Teste 2: Alerta de praga
    print("\n🧪 Teste 2: Detecção de Praga (Fase 6 - YOLO)")
    result2 = manager.notify_pest_detection(
        pest_name="Lagarta do Cartucho",
        confidence=0.94,
        image_path="/data/detections/img_001.jpg",
        location="Setor B - Milho"
    )
    print(f"   ✅ Resultado: {result2['success']} | Modo: {result2['mode']}")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats = manager.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # ========================================
    # EXEMPLO 2: Classe legada (compatibilidade)
    # ========================================
    print("\n" + "=" * 70)
    print("📋 EXEMPLO 2: Usando AWSManager (Classe Legada)")
    print("-" * 70)
    
    legacy_manager = AWSManager(region_name='us-east-1')
    
    # Mostra status
    status = legacy_manager.get_status()
    print(f"\n📊 Status AWS (legado):")
    print(f"   AWS Configurado: {status['aws_configured']}")
    print(f"   Modo Simulação: {status['simulate_mode']}")
    
    # Teste com classe legada
    print("\n🧪 Teste: Alerta legado")
    result3 = legacy_manager.send_soil_moisture_alert(
        humidity=25.0,
        threshold=30.0
    )
    print(f"   ✅ Resultado: {result3['success']}")
    
    print("\n" + "=" * 70)
    print("✅ Demonstração concluída!")
    print("\n💡 RECOMENDAÇÃO: Use AWSAlertManager para novos projetos")
    print("=" * 70 + "\n")

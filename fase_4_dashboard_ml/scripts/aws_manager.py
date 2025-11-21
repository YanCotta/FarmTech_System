"""
AWS Manager - Gerenciador de Serviços AWS para FarmTech Solutions

Este módulo fornece integração com serviços AWS, especialmente SNS para alertas.
Implementa fallback de simulação quando credenciais AWS não estão disponíveis.

Baseado no desafio "Ir Além 1" - Integração AWS
"""

import logging
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


class AWSManager:
    """
    Gerenciador de serviços AWS para o sistema FarmTech.
    
    Esta classe gerencia a comunicação com serviços AWS, particularmente
    SNS (Simple Notification Service) para envio de alertas. Implementa
    um sistema de fallback que simula o envio quando credenciais não
    estão disponíveis, permitindo desenvolvimento e testes sem AWS.
    
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
        try:
            import boto3
            from botocore.exceptions import NoCredentialsError, PartialCredentialsError
            
            # Tenta criar cliente SNS
            self.sns_client = boto3.client('sns', region_name=self.region_name)
            
            # Testa as credenciais fazendo uma chamada simples
            self.sns_client.list_topics(MaxResults=1)
            
            logger.info(f"✅ Cliente AWS SNS inicializado com sucesso na região {self.region_name}")
            return True
            
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.warning(f"⚠️ Credenciais AWS não encontradas: {e}")
            logger.info("🔄 Modo simulação será ativado")
            self.sns_client = None
            return False
            
        except ImportError:
            logger.warning("⚠️ Biblioteca boto3 não instalada")
            logger.info("💡 Execute: pip install boto3")
            logger.info("🔄 Modo simulação será ativado")
            self.sns_client = None
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao inicializar cliente AWS: {e}")
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


# Exemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("AWS Manager - Sistema de Alertas FarmTech Solutions")
    print("=" * 70)
    
    # Cria gerenciador (tentará usar AWS real, mas fará fallback para simulação)
    manager = AWSManager(region_name='us-east-1')
    
    # Mostra status
    status = manager.get_status()
    print(f"\n📊 Status da conexão AWS:")
    print(f"   AWS Configurado: {status['aws_configured']}")
    print(f"   Modo Simulação: {status['simulate_mode']}")
    print(f"   Região: {status['region']}\n")
    
    # Teste 1: Alerta de umidade
    print("\n🧪 Teste 1: Alerta de umidade do solo")
    result1 = manager.send_soil_moisture_alert(humidity=25.0, threshold=30.0)
    print(f"Resultado: {'✅ Sucesso' if result1['success'] else '❌ Falha'}")
    
    # Teste 2: Alerta de praga
    print("\n🧪 Teste 2: Alerta de detecção de praga")
    result2 = manager.send_pest_detection_alert(
        pest_type="Lagarta",
        confidence=85.5,
        location="Setor B - Plantação de Milho"
    )
    print(f"Resultado: {'✅ Sucesso' if result2['success'] else '❌ Falha'}")
    
    # Teste 3: Alerta genérico
    print("\n🧪 Teste 3: Alerta genérico do sistema")
    result3 = manager.send_system_alert(
        alert_type="Manutenção Programada",
        details="Sistema de irrigação será desligado amanhã às 14h para manutenção",
        level=AlertLevel.INFO
    )
    print(f"Resultado: {'✅ Sucesso' if result3['success'] else '❌ Falha'}")
    
    print("\n" + "=" * 70)
    print("✅ Testes concluídos!")
    print("=" * 70)

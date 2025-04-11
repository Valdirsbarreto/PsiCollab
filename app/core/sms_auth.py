import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
from dotenv import load_dotenv
import httpx
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi import HTTPException
import redis

# Configuração de logging mais detalhada
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para arquivo
file_handler = logging.FileHandler('sms_auth.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
SMS_CODE_EXPIRY_MINUTES = int(os.getenv("SMS_CODE_EXPIRY_MINUTES", 5))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# Configurações do Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SID = os.getenv("TWILIO_VERIFY_SID")

# Configuração Redis
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

# Tempo de expiração do cache (30 minutos)
CACHE_EXPIRATION = 1800

# Log das configurações (mascarando o token por segurança)
logger.debug("=== Configurações do Twilio ===")
logger.debug(f"TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID}")
logger.debug(f"TWILIO_AUTH_TOKEN: {'*' * 8 if TWILIO_AUTH_TOKEN else 'Não configurado'}")
logger.debug(f"TWILIO_VERIFY_SID: {TWILIO_VERIFY_SID}")

# Validações das configurações
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SID]):
    logger.error("Configurações do Twilio incompletas")
    raise ValueError("Configurações do Twilio incompletas. Verifique ACCOUNT_SID, AUTH_TOKEN e VERIFY_SID")

# Inicializa o cliente Twilio
try:
    logger.debug("Iniciando cliente Twilio...")
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    # Testa a conexão
    logger.debug("Testando conexão com Twilio...")
    account = twilio_client.api.accounts(TWILIO_ACCOUNT_SID).fetch()
    logger.info(f"Cliente Twilio inicializado com sucesso. Status da conta: {account.status}")
except Exception as e:
    logger.error(f"Erro ao inicializar cliente Twilio: {str(e)}")
    twilio_client = None

# Armazenamento temporário de códigos (em produção, usar Redis ou banco de dados)
sms_codes: Dict[str, Dict] = {}

def generate_verification_code(length: int = 6) -> str:
    """Gera um código de verificação numérico"""
    return ''.join(random.choices(string.digits, k=length))

async def send_verification_code(phone_number: str) -> bool:
    """
    Envia código de verificação via Twilio Verify
    """
    logger.info(f"Iniciando envio de código para {phone_number}")
    try:
        # Validação do número de telefone
        if not phone_number or not phone_number.startswith('+'):
            logger.error(f"Número de telefone inválido: {phone_number}")
            raise ValueError("Número de telefone deve começar com '+' e incluir código do país")

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.debug("Cliente Twilio inicializado com sucesso")
        
        verification = client.verify \
            .v2.services(TWILIO_VERIFY_SID) \
            .verifications \
            .create(to=phone_number, channel="sms")
            
        logger.info(f"Código enviado com sucesso para {phone_number}. Status: {verification.status}")
        return True
        
    except TwilioRestException as e:
        logger.error(f"Erro Twilio ao enviar código: {str(e)}")
        raise ValueError(f"Erro ao enviar código: {str(e)}")
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar código: {str(e)}")
        raise

async def verify_code(phone_number: str, code: str) -> bool:
    """
    Verifica código recebido via Twilio Verify
    """
    logger.info(f"Iniciando verificação de código para {phone_number}")
    try:
        # Validação do número de telefone e código
        if not phone_number or not phone_number.startswith('+'):
            logger.error(f"Número de telefone inválido: {phone_number}")
            raise ValueError("Número de telefone deve começar com '+' e incluir código do país")
            
        if not code or len(code) != 6 or not code.isdigit():
            logger.error(f"Código inválido: {code}")
            raise ValueError("Código deve conter 6 dígitos")

        # Tenta conectar ao Redis primeiro
        try:
            logger.debug("Testando conexão com Redis...")
            redis_client.ping()
            logger.info("Conexão com Redis estabelecida com sucesso")
        except redis.ConnectionError as e:
            logger.error(f"Erro ao conectar com Redis: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro de conexão com o serviço de cache")
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.debug("Cliente Twilio inicializado para verificação")
        
        verification_check = client.verify \
            .v2.services(TWILIO_VERIFY_SID) \
            .verification_checks \
            .create(to=phone_number, code=code)
            
        is_valid = verification_check.status == "approved"
        if is_valid:
            # Armazena o número verificado no cache
            try:
                cache_key = f"verified_phone_{phone_number}"
                redis_client.setex(cache_key, CACHE_EXPIRATION, "1")
                logger.info(f"Número {phone_number} armazenado no cache por {CACHE_EXPIRATION} segundos")
            except redis.RedisError as e:
                logger.error(f"Erro ao armazenar no cache: {str(e)}")
                # Continua mesmo se o cache falhar
            
        logger.info(f"Verificação concluída para {phone_number}. Status: {verification_check.status}")
        return is_valid
        
    except TwilioRestException as e:
        logger.error(f"Erro Twilio ao verificar código: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erro ao verificar código: {str(e)}")
    except redis.RedisError as e:
        logger.error(f"Erro Redis: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro no serviço de cache")
    except Exception as e:
        logger.error(f"Erro inesperado ao verificar código: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

def create_phone_token(phone_number: str) -> str:
    """Cria um token JWT para o número de telefone verificado"""
    logger.debug(f"Criando token JWT para o número {phone_number}")
    
    token_data = {
        "sub": phone_number,
        "exp": datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", 60)))
    }
    
    token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Token JWT criado com sucesso para {phone_number}")
    return token

def validate_phone_token(token: str) -> Optional[str]:
    """Valida o token JWT e retorna o número de telefone"""
    logger.debug("Validando token JWT")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        phone_number = payload["sub"]
        logger.debug(f"Token JWT válido para o número {phone_number}")
        return phone_number
    except jwt.PyJWTError as e:
        logger.error(f"Erro ao validar token JWT: {str(e)}")
        return None 
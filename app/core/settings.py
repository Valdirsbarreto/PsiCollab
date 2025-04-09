"""
Configurações do PsiCollab.
"""
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    # Configurações básicas
    APP_NAME: str = "PsiCollab"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # Configurações de segurança
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    JWT_ALGORITHM: str = "HS256"
    
    # Configurações do OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 4000
    
    # Configurações do Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

# Criar instância global de configurações
settings = Settings() 
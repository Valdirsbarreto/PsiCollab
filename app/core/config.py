"""
Configurações do PsiCollab.
"""
from typing import Optional, Dict, Any
import os
from pydantic_settings import BaseSettings
import logging

# Definição da classe de configurações
class Settings(BaseSettings):
    """
    Configurações da aplicação usando variáveis de ambiente
    """
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"
    }
    
    # Configurações básicas
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "PsiCollab"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    
    # Configurações do OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 4000
    
    # Configurações do Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    COLLECTION_NAME: str = "knowledge_base"
    VECTOR_SIZE: int = 1536  # Tamanho do vetor para modelo GPT
    VECTOR_DB_URL: str = "http://localhost:6333"
    
    # Configurações de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/app.log"
    
    # Configurações do Google OAuth2
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/auth/google/callback"
    
    # Configurações do banco de dados
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./psicollab.db")
    DATABASE_CONNECT_ARGS: Dict[str, Any] = {"check_same_thread": False}  # Para SQLite

# Criação da instância de configurações
settings = Settings()

# Definição das exportações
__all__ = ['settings', 'Settings'] 
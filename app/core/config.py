"""
Configurações do sistema PsiCollab.
"""
import os
from typing import Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Configurações do sistema.
    """
    # Diretórios
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    KNOWLEDGE_BASE_DIR: str = os.path.join(BASE_DIR, "data", "knowledge_base")
    
    # APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_URL: str = "https://api.openai.com/v1"
    EMBEDDING_API_URL: str = f"{OPENAI_API_URL}/embeddings"
    VECTOR_DB_URL: str = os.getenv("VECTOR_DB_URL", "http://localhost:6333")
    
    # PostgreSQL
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "psicollab")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "psicollab")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # MongoDB
    MONGO_USER: str = os.getenv("MONGO_USER", "psicollab")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD", "")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    
    # Configurações de Processamento
    BATCH_SIZE: int = 10
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    
    # Configurações de Cache
    CACHE_TTL: int = 24 * 60 * 60  # 24 horas em segundos
    CACHE_MAX_SIZE: int = 1000
    
    # Configurações de Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR: str = os.path.join(BASE_DIR, "..", "logs")
    
    # Configurações de Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "sua_chave_jwt_aqui")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALLOWED_HOSTS: list = ["*"]
    
    # Configurações da Aplicação
    APP_NAME: str = os.getenv("APP_NAME", "PsiCollab")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="allow")

# Instância global das configurações
settings = Settings() 
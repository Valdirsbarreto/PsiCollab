"""
Testes para as configurações da aplicação.
"""
import pytest
from pydantic import ValidationError
from app.core.config import Settings, settings

def test_settings_default_values():
    """Testa os valores padrão das configurações."""
    test_settings = Settings()
    
    # Configurações gerais
    assert test_settings.APP_NAME == "PsiCollab"
    assert test_settings.DEBUG is False
    
    # Configurações de segurança
    assert test_settings.SECRET_KEY == ""
    assert test_settings.ALGORITHM == "HS256"
    assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    
    # Configurações do OpenAI
    assert test_settings.OPENAI_API_KEY == ""
    assert test_settings.OPENAI_MODEL == "gpt-4"
    assert test_settings.OPENAI_TEMPERATURE == 0.7
    assert test_settings.OPENAI_MAX_TOKENS == 4000
    
    # Configurações de banco de dados
    assert test_settings.POSTGRES_USER == "postgres"
    assert test_settings.POSTGRES_PASSWORD == "postgres"
    assert test_settings.POSTGRES_SERVER == "localhost"
    assert test_settings.POSTGRES_PORT == "5432"
    assert test_settings.POSTGRES_DB == "psicollab"
    
    # Configurações do MongoDB
    assert test_settings.MONGODB_URL == "mongodb://localhost:27017"
    assert test_settings.MONGODB_DB == "psicollab"
    
    # Configurações do Vector DB
    assert test_settings.VECTOR_DB_URL == "http://localhost:8080"

def test_settings_custom_values():
    """Testa a configuração com valores personalizados."""
    custom_settings = Settings(
        APP_NAME="TestApp",
        DEBUG=True,
        SECRET_KEY="test_key",
        OPENAI_API_KEY="test_openai_key",
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_pass",
        POSTGRES_SERVER="test_server",
        POSTGRES_PORT="5433",
        POSTGRES_DB="test_db",
        MONGODB_URL="mongodb://test:27017",
        MONGODB_DB="test_db",
        VECTOR_DB_URL="http://test:8080"
    )
    
    # Verifica valores personalizados
    assert custom_settings.APP_NAME == "TestApp"
    assert custom_settings.DEBUG is True
    assert custom_settings.SECRET_KEY == "test_key"
    assert custom_settings.OPENAI_API_KEY == "test_openai_key"
    assert custom_settings.POSTGRES_USER == "test_user"
    assert custom_settings.POSTGRES_PASSWORD == "test_pass"
    assert custom_settings.POSTGRES_SERVER == "test_server"
    assert custom_settings.POSTGRES_PORT == "5433"
    assert custom_settings.POSTGRES_DB == "test_db"
    assert custom_settings.MONGODB_URL == "mongodb://test:27017"
    assert custom_settings.MONGODB_DB == "test_db"
    assert custom_settings.VECTOR_DB_URL == "http://test:8080"

def test_settings_database_url():
    """Testa a geração automática da URL do banco de dados."""
    test_settings = Settings(
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_pass",
        POSTGRES_SERVER="test_server",
        POSTGRES_PORT="5433",
        POSTGRES_DB="test_db"
    )
    
    expected_url = "postgresql://test_user:test_pass@test_server:5433/test_db"
    assert test_settings.DATABASE_URL == expected_url

def test_settings_custom_database_url():
    """Testa a configuração de uma URL de banco de dados personalizada."""
    custom_url = "postgresql://custom:pass@custom:5432/custom_db"
    test_settings = Settings(DATABASE_URL=custom_url)
    
    assert test_settings.DATABASE_URL == custom_url

def test_settings_validation():
    """Testa a validação das configurações."""
    # Teste de tipo inválido
    with pytest.raises(ValidationError):
        Settings(DEBUG="invalid")
    
    # Teste de valor inválido para temperatura
    with pytest.raises(ValidationError):
        Settings(OPENAI_TEMPERATURE=2.0)
    
    # Teste de valor inválido para tokens
    with pytest.raises(ValidationError):
        Settings(OPENAI_MAX_TOKENS=-1)

def test_settings_global_instance():
    """Testa a instância global de configurações."""
    assert isinstance(settings, Settings)
    assert settings.APP_NAME == "PsiCollab"
    assert settings.DEBUG is False 
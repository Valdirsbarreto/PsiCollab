"""
Configuração do banco de dados do PsiCollab.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configuração da URL do banco de dados
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Criação do motor do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=settings.DATABASE_CONNECT_ARGS
)

# Criação da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """
    Função para obter uma sessão de banco de dados.
    Gerencia o ciclo de vida da sessão e garante que ela seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
"""
Script para inicializar o banco de dados.
Cria as tabelas necessárias se não existirem.
"""
import sys
import os
import logging
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from app.core.database import engine
from app.models.user import Base

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas.
    """
    try:
        logger.info("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    logger.info("Inicializando banco de dados...")
    if init_db():
        logger.info("Banco de dados inicializado com sucesso.")
    else:
        logger.error("Falha ao inicializar banco de dados.")
        sys.exit(1) 
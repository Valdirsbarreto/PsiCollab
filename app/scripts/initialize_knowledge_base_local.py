"""
Script para inicializar a base de conhecimento localmente.
Esta versão armazena embeddings em arquivos JSON locais em vez de usar o Qdrant.
"""
import argparse
import logging
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.knowledge_manager_local import KnowledgeManagerLocal
from app.core.embedding_generator import EmbeddingGenerator

# Configuração do logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def initialize_knowledge_base(mode: str = "initialize") -> None:
    """
    Inicializa a base de conhecimento localmente.
    
    Args:
        mode: Modo de inicialização ("initialize" ou "update")
    """
    try:
        # Verifica se o diretório existe
        knowledge_base_dir = Path(settings.KNOWLEDGE_BASE_DIR)
        if not knowledge_base_dir.exists():
            logger.error(f"Diretório {knowledge_base_dir} não encontrado")
            return

        # Inicializa os gerenciadores
        knowledge_manager = KnowledgeManagerLocal()
        embedding_generator = EmbeddingGenerator()

        # Processa os arquivos JSON
        for json_file in knowledge_base_dir.glob("*.json"):
            logger.info(f"Processando arquivo: {json_file}")
            
            # Carrega os dados
            documents = knowledge_manager.load_documents(json_file)
            
            if not documents:
                logger.warning(f"Nenhum documento encontrado em {json_file}")
                continue
                
            logger.info(f"Carregados {len(documents)} documentos de {json_file}")
            
            # Gera os embeddings
            embeddings = embedding_generator.generate_embeddings(documents)
            
            # Armazena em arquivo JSON local
            knowledge_manager.store_documents(documents, embeddings)
            
            logger.info(f"Arquivo {json_file} processado com sucesso")

        logger.info("Base de conhecimento inicializada com sucesso")

    except Exception as e:
        logger.error(f"Erro ao inicializar base de conhecimento: {str(e)}")
        raise

def main():
    """
    Função principal do script.
    """
    parser = argparse.ArgumentParser(description="Inicializa a base de conhecimento")
    parser.add_argument(
        "--mode",
        type=str,
        default="initialize",
        choices=["initialize", "update"],
        help="Modo de inicialização"
    )
    
    args = parser.parse_args()
    initialize_knowledge_base(args.mode)

if __name__ == "__main__":
    main() 
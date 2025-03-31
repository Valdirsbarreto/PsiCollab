"""
Gerenciador da Base de Conhecimento Local do PsiCollab.
Versão que armazena embeddings em arquivos JSON locais em vez de usar o Qdrant.
"""
from typing import Dict, Any, List, Optional
import os
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from app.core.embedding_generator import EmbeddingGenerator
from app.core.config import settings

# Configuração de logging
logger = logging.getLogger(__name__)

class KnowledgeManagerLocal:
    """
    Gerenciador da Base de Conhecimento Local.
    Versão que armazena embeddings em arquivos JSON locais em vez de usar o Qdrant.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de conhecimento local."""
        self.knowledge_dir = settings.KNOWLEDGE_BASE_DIR
        self.embeddings_dir = os.path.join(settings.BASE_DIR, "data", "embeddings")
        self.embedding_generator = EmbeddingGenerator()
        self.base_dir = Path(settings.KNOWLEDGE_BASE_DIR)
        
        # Verificar e criar diretórios se não existirem
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            
        if not os.path.exists(self.embeddings_dir):
            os.makedirs(self.embeddings_dir)
    
    def load_documents(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Carrega documentos de um arquivo JSON.
        
        Args:
            file_path: Caminho do arquivo JSON
            
        Returns:
            Lista de documentos carregados
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            return documents
        except Exception as e:
            logger.error(f"Erro ao carregar documentos: {str(e)}")
            return []

    def store_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]) -> None:
        """
        Armazena documentos e seus embeddings em um arquivo JSON local.
        
        Args:
            documents: Lista de documentos
            embeddings: Lista de embeddings correspondentes
        """
        try:
            # Preparar documentos com embeddings
            enriched_documents = []
            for doc, emb in zip(documents, embeddings):
                # Gera um UUID para cada documento
                doc_id = str(uuid.uuid4())
                enriched_doc = doc.copy()
                enriched_doc["uuid"] = doc_id
                enriched_doc["embedding"] = emb
                enriched_doc["timestamp"] = datetime.now().isoformat()
                enriched_documents.append(enriched_doc)

            # Determinar o nome do arquivo baseado no tipo do documento
            if documents and "tipo" in documents[0]:
                file_name = f"{documents[0]['tipo']}_embeddings.json"
            else:
                file_name = f"embeddings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            file_path = os.path.join(self.embeddings_dir, file_name)
            
            # Verificar se o arquivo já existe
            existing_docs = []
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_docs = json.load(f)
                except:
                    existing_docs = []
            
            # Adicionar novos documentos
            all_docs = existing_docs + enriched_documents
            
            # Salvar no arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(all_docs, f, ensure_ascii=False, indent=2)

            logger.info(f"Armazenados {len(documents)} documentos com embeddings no arquivo {file_path}")

        except Exception as e:
            logger.error(f"Erro ao armazenar documentos localmente: {str(e)}")
            raise 
"""
Motor de Busca Semântica para o PsiCollab.
Responsável por processar consultas em linguagem natural e recuperar
documentos relevantes da base de conhecimento.
"""
from typing import Dict, Any, List, Optional, Tuple
import logging
import uuid
import json
from datetime import datetime

from app.core.config import settings
from app.core.embedding_generator import EmbeddingGenerator
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configuração de logging
logger = logging.getLogger(__name__)

class SearchEngine:
    """
    Motor de Busca Semântica.
    Processa consultas em linguagem natural, gera embeddings e 
    recupera documentos relevantes da base de conhecimento.
    """
    
    def __init__(self):
        """Inicializa o motor de busca."""
        self.embedding_generator = EmbeddingGenerator()
        self.client = QdrantClient(settings.VECTOR_DB_URL)
        self.collection_name = "knowledge_base"
        self.search_params = models.SearchParams(
            hnsw_ef=128,
            exact=False
        )
        
    async def search(
        self, 
        query: str, 
        limit: int = 5, 
        tipo_filtro: Optional[str] = None,
        min_score: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Realiza uma busca semântica na base de conhecimento.
        
        Args:
            query: Consulta em linguagem natural
            limit: Número máximo de resultados
            tipo_filtro: Filtro opcional por tipo de documento
            min_score: Pontuação mínima de similaridade (0-1)
            
        Returns:
            Lista de documentos relevantes ordenados por similaridade
        """
        try:
            # Gera embedding para a consulta
            query_embedding = self.embedding_generator.generate_embeddings([{"conteudo": query}])[0]
            
            # Prepara o filtro se especificado
            filter_param = None
            if tipo_filtro:
                filter_param = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tipo",
                            match=models.MatchValue(value=tipo_filtro)
                        )
                    ]
                )
            
            # Realiza a busca no Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=filter_param,
                search_params=self.search_params,
                with_payload=True,
                with_vectors=False,
                score_threshold=min_score
            )
            
            # Processa os resultados
            results = []
            for result in search_results:
                doc = result.payload
                doc["score"] = result.score
                results.append(doc)
            
            logger.info(f"Busca por '{query}' retornou {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"Erro ao realizar busca: {str(e)}")
            return []
    
    def search_by_type(
        self, 
        query: str, 
        tipo: str, 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Realiza uma busca semântica filtrando por tipo de documento.
        
        Args:
            query: Consulta em linguagem natural
            tipo: Tipo de documento para filtrar
            limit: Número máximo de resultados
            
        Returns:
            Lista de documentos relevantes do tipo especificado
        """
        return self.search(query, limit, tipo_filtro=tipo)
    
    def search_multi_query(
        self, 
        queries: List[str], 
        limit_per_query: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Realiza múltiplas consultas e combina os resultados.
        Útil para consultas complexas que podem ser divididas.
        
        Args:
            queries: Lista de consultas relacionadas
            limit_per_query: Número máximo de resultados por consulta
            
        Returns:
            Lista combinada de documentos relevantes sem duplicatas
        """
        all_results = []
        seen_ids = set()
        
        for query in queries:
            results = self.search(query, limit=limit_per_query)
            
            for result in results:
                # Evita adicionar documentos duplicados
                doc_id = result.get("id", result.get("uuid", None))
                if doc_id and doc_id not in seen_ids:
                    seen_ids.add(doc_id)
                    all_results.append(result)
        
        # Ordena os resultados por pontuação
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return all_results
    
    def rerank_results(
        self, 
        query: str, 
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Reordena os resultados aplicando um modelo de reranking.
        Esta é uma implementação simplificada que pode ser expandida.
        
        Args:
            query: Consulta original
            results: Lista de resultados para reordenar
            
        Returns:
            Lista de resultados reordenados
        """
        # Implementação futura: integrar um modelo de reranking mais sofisticado
        return results
    
    def log_search(self, query: str, results: List[Dict[str, Any]], user_id: Optional[str] = None) -> None:
        """
        Registra uma busca para análise e melhoria do sistema.
        
        Args:
            query: Consulta realizada
            results: Resultados retornados
            user_id: Identificador opcional do usuário
        """
        try:
            log_entry = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "num_results": len(results),
                "user_id": user_id or "anonymous",
                "top_result_id": results[0].get("id") if results else None,
                "top_result_score": results[0].get("score") if results else None
            }
            
            # Aqui você pode implementar o armazenamento do log
            # Por exemplo, salvar em um arquivo ou banco de dados
            
            logger.debug(f"Busca registrada: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Erro ao registrar busca: {str(e)}")
            # Não propaga a exceção para não interferir na experiência do usuário 
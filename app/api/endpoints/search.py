"""
Endpoints para busca semântica na base de conhecimento.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.search_engine import SearchEngine

# Cria o roteador
router = APIRouter()

# Modelos de dados
class SearchQuery(BaseModel):
    """Modelo para consulta de busca."""
    query: str = Field(..., description="Consulta em linguagem natural")
    limit: int = Field(5, description="Número máximo de resultados", ge=1, le=20)
    tipo: Optional[str] = Field(None, description="Filtro por tipo de documento")
    min_score: float = Field(0.7, description="Pontuação mínima de similaridade", ge=0, le=1)

class MultiSearchQuery(BaseModel):
    """Modelo para consulta múltipla."""
    queries: List[str] = Field(..., description="Lista de consultas relacionadas")
    limit_per_query: int = Field(3, description="Número máximo de resultados por consulta", ge=1, le=10)

class SearchResult(BaseModel):
    """Modelo para resultado de busca."""
    id: str = Field(..., description="Identificador do documento")
    tipo: str = Field(..., description="Tipo do documento")
    conteudo: str = Field(..., description="Conteúdo do documento")
    score: float = Field(..., description="Pontuação de similaridade")
    metadata: Dict[str, Any] = Field(..., description="Metadados do documento")

class SearchResponse(BaseModel):
    """Modelo para resposta de busca."""
    results: List[SearchResult] = Field([], description="Resultados da busca")
    count: int = Field(0, description="Número de resultados")
    query: str = Field(..., description="Consulta original")

# Dependência para obter o motor de busca
def get_search_engine():
    """Retorna uma instância do motor de busca."""
    return SearchEngine()

@router.post("/query", response_model=SearchResponse, summary="Busca semântica")
async def search(
    search_query: SearchQuery,
    search_engine: SearchEngine = Depends(get_search_engine)
):
    """
    Realiza uma busca semântica na base de conhecimento.
    
    A consulta é processada pelo motor de busca semântica, que:
    1. Gera embeddings para a consulta
    2. Busca documentos similares na base de conhecimento
    3. Retorna os documentos ordenados por similaridade
    
    Os resultados podem ser filtrados por tipo e pontuação mínima.
    """
    results = await search_engine.search(
        query=search_query.query,
        limit=search_query.limit,
        tipo_filtro=search_query.tipo,
        min_score=search_query.min_score
    )
    
    # Registra a busca para análise futura
    search_engine.log_search(search_query.query, results)
    
    # Formata a resposta
    return SearchResponse(
        results=results,
        count=len(results),
        query=search_query.query
    )

@router.post("/multi-query", response_model=SearchResponse, summary="Busca múltipla")
async def multi_search(
    multi_query: MultiSearchQuery,
    search_engine: SearchEngine = Depends(get_search_engine)
):
    """
    Realiza múltiplas consultas e combina os resultados.
    
    Útil para consultas complexas que podem ser divididas em
    sub-consultas mais específicas.
    """
    results = search_engine.search_multi_query(
        queries=multi_query.queries,
        limit_per_query=multi_query.limit_per_query
    )
    
    # Registra a busca para análise futura
    query_str = " | ".join(multi_query.queries)
    search_engine.log_search(query_str, results)
    
    # Formata a resposta
    return SearchResponse(
        results=results,
        count=len(results),
        query=query_str
    )

@router.get("/types", response_model=List[str], summary="Tipos de documentos")
async def get_types(
    search_engine: SearchEngine = Depends(get_search_engine)
):
    """
    Retorna a lista de todos os tipos de documentos disponíveis.
    
    Útil para filtrar buscas por tipo específico de documento.
    """
    # Implementação básica - será expandida para buscar do banco de dados
    return [
        "adulto", "adolescente", "infantil", "gerontologico", 
        "personalidade", "inteligencia", "comportamento", 
        "projetivo", "objetivo", "neuropsicologico"
    ] 
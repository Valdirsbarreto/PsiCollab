"""
Motor de Retrieval-Augmented Generation (RAG) para enriquecer interpretações com conhecimento específico.
"""
from typing import Dict, Any, List, Optional
import json
import aiohttp
from datetime import datetime
from app.core.config import settings
from app.core.audit import AuditoriaManager, TipoOperacao, NivelSensibilidade

class RAGEngine:
    """
    Motor de Retrieval-Augmented Generation para enriquecer interpretações
    com conhecimento específico da área de psicologia.
    """
    
    def __init__(self):
        """Inicializa o motor RAG."""
        self.vector_db_url = settings.VECTOR_DB_URL
        self.cache = {}  # Cache simples para consultas repetidas
        self.audit_manager = AuditoriaManager()
    
    async def buscar_conhecimento(
        self,
        test_type: str,
        contexto: Dict[str, Any],
        usuario_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Busca conhecimento relevante baseado no tipo de teste e contexto.
        
        Args:
            test_type: Tipo do teste
            contexto: Contexto da consulta
            usuario_id: ID do usuário (opcional)
            ip_address: Endereço IP do usuário (opcional)
            user_agent: User Agent do navegador (opcional)
            top_k: Número de documentos a retornar
            
        Returns:
            Lista de documentos relevantes
        """
        # Gera uma chave de cache
        cache_key = f"{test_type}_{json.dumps(contexto)}_{top_k}"
        
        # Verifica se há resultados em cache
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Registra a operação na auditoria
        self._registro_atual = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.PROCESSAMENTO,
            nivel_sensibilidade=NivelSensibilidade.ALTO,
            usuario_id=usuario_id or "sistema",
            recurso="rag_engine",
            detalhes={
                "test_type": test_type,
                "contexto": contexto,
                "top_k": top_k
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        try:
            # Prepara a query para o Vector DB
            query = {
                "test_type": test_type,
                "contexto": contexto,
                "top_k": top_k
            }
            
            # Faz a requisição para o Vector DB
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.vector_db_url}/search",
                    json=query,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        resultados = await response.json()
                        
                        # Atualiza o cache
                        self.cache[cache_key] = resultados
                        
                        return resultados
                    else:
                        raise Exception(f"Erro ao buscar conhecimento: {response.status}")
                        
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                self._registro_atual,
                f"Erro ao buscar conhecimento: {str(e)}"
            )
            return []
    
    def enriquecer_prompt(
        self,
        prompt_base: str,
        documentos: List[Dict[str, Any]]
    ) -> str:
        """
        Enriquece o prompt com conhecimento específico.
        
        Args:
            prompt_base: Prompt original
            documentos: Lista de documentos relevantes
            
        Returns:
            Prompt enriquecido
        """
        if not documentos:
            return prompt_base
            
        # Estrutura o conhecimento específico
        conhecimento = "\n\nConhecimento Específico:\n"
        for doc in documentos:
            conhecimento += f"\n{doc['conteudo']}\n"
            if doc.get('metadata'):
                conhecimento += f"Fonte: {doc['metadata'].get('fonte', 'N/A')}\n"
                conhecimento += f"Ano: {doc['metadata'].get('ano', 'N/A')}\n"
        
        return f"{prompt_base}{conhecimento}"
    
    def limpar_cache(self) -> None:
        """Limpa o cache de consultas."""
        self.cache.clear() 
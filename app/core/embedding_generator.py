"""
Gerador de Embeddings para a Base de Conhecimento do PsiCollab.
Responsável por processar documentos de conhecimento psicológico 
e gerar vetores para armazenamento na Vector DB.
"""
from typing import Dict, Any, List, Optional, Tuple
import os
import json
import asyncio
import logging
from datetime import datetime
import aiohttp
import numpy as np
from openai import OpenAI
from app.core.config import settings
from app.core.audit import AuditoriaManager, TipoOperacao, NivelSensibilidade

# Configuração de logging
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Gerador de embeddings para a base de conhecimento.
    Processa documentos de conhecimento psicológico e gera vetores
    para armazenamento na Vector DB.
    """
    
    def __init__(self):
        """Inicializa o gerador de embeddings."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_db_url = settings.VECTOR_DB_URL
        self.audit_manager = AuditoriaManager()
        self.batch_size = settings.BATCH_SIZE
    
    async def gerar_embedding(
        self, 
        texto: str,
        usuario_id: Optional[str] = None
    ) -> List[float]:
        """
        Gera um embedding para um texto usando a API de embeddings.
        
        Args:
            texto: Texto para o qual gerar o embedding
            usuario_id: ID do usuário para auditoria
            
        Returns:
            Lista de floats representando o embedding do texto
        """
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.PROCESSAMENTO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="embedding_generator",
            detalhes={
                "operacao": "gerar_embedding",
                "tamanho_texto": len(texto)
            }
        )
        
        try:
            # Requisição para a API de embeddings
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.embedding_api_url,
                    json={"texto": texto},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        resultado = await response.json()
                        return resultado["embedding"]
                    else:
                        erro = await response.text()
                        raise Exception(f"Erro ao gerar embedding: {response.status} - {erro}")
        
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao gerar embedding: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao gerar embedding: {str(e)}")
            # Retorna um embedding vazio em caso de erro
            return []
    
    async def processar_documento(
        self,
        documento: Dict[str, Any],
        usuario_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processa um documento, gerando seu embedding e preparando
        para armazenamento na Vector DB.
        
        Args:
            documento: Documento a ser processado
            usuario_id: ID do usuário para auditoria
            
        Returns:
            Documento processado com embedding
        """
        # Valida o documento
        if not self._validar_documento(documento):
            raise ValueError("Documento inválido: campos obrigatórios ausentes")
        
        # Gera o embedding para o documento
        embedding = await self.gerar_embedding(
            documento["conteudo"],
            usuario_id
        )
        
        # Adiciona o embedding ao documento
        documento_processado = documento.copy()
        documento_processado["embedding"] = embedding
        documento_processado["data_processamento"] = datetime.now().isoformat()
        
        return documento_processado
    
    def _validar_documento(self, documento: Dict[str, Any]) -> bool:
        """
        Valida se o documento contém os campos obrigatórios.
        
        Args:
            documento: Documento a ser validado
            
        Returns:
            True se o documento for válido, False caso contrário
        """
        campos_obrigatorios = ["id", "conteudo", "tipo", "metadata"]
        return all(campo in documento for campo in campos_obrigatorios)
        
    async def processar_lote(
        self,
        documentos: List[Dict[str, Any]],
        usuario_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Processa um lote de documentos em paralelo.
        
        Args:
            documentos: Lista de documentos a serem processados
            usuario_id: ID do usuário para auditoria
            
        Returns:
            Lista de documentos processados
        """
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.PROCESSAMENTO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="embedding_generator",
            detalhes={
                "operacao": "processar_lote",
                "quantidade_documentos": len(documentos)
            }
        )
        
        try:
            # Processa os documentos em paralelo
            tarefas = [
                self.processar_documento(doc, usuario_id)
                for doc in documentos
            ]
            
            return await asyncio.gather(*tarefas)
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao processar lote: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao processar lote: {str(e)}")
            # Retorna uma lista vazia em caso de erro
            return []
    
    async def armazenar_na_vector_db(
        self,
        documentos_processados: List[Dict[str, Any]],
        usuario_id: Optional[str] = None
    ) -> bool:
        """
        Armazena documentos processados na Vector DB.
        
        Args:
            documentos_processados: Lista de documentos processados
            usuario_id: ID do usuário para auditoria
            
        Returns:
            True se o armazenamento for bem-sucedido, False caso contrário
        """
        if not documentos_processados:
            return False
            
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.ARMAZENAMENTO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="vector_db",
            detalhes={
                "operacao": "armazenar_documentos",
                "quantidade_documentos": len(documentos_processados)
            }
        )
        
        try:
            # Faz a requisição para a Vector DB
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.vector_db_url}/store",
                    json={"documentos": documentos_processados},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        # Log do sucesso
                        logger.info(f"Armazenados {len(documentos_processados)} documentos na Vector DB")
                        return True
                    else:
                        erro = await response.text()
                        raise Exception(f"Erro ao armazenar na Vector DB: {response.status} - {erro}")
        
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao armazenar na Vector DB: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao armazenar na Vector DB: {str(e)}")
            return False
            
    async def processar_arquivo_json(
        self,
        caminho_arquivo: str,
        usuario_id: Optional[str] = None
    ) -> Tuple[int, int]:
        """
        Processa um arquivo JSON contendo documentos de conhecimento.
        
        Args:
            caminho_arquivo: Caminho para o arquivo JSON
            usuario_id: ID do usuário para auditoria
            
        Returns:
            Tupla (total de documentos, documentos processados com sucesso)
        """
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.PROCESSAMENTO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="embedding_generator",
            detalhes={
                "operacao": "processar_arquivo_json",
                "arquivo": caminho_arquivo
            }
        )
        
        try:
            # Carrega o arquivo JSON
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                documentos = json.load(f)
            
            total_documentos = len(documentos)
            documentos_processados = 0
            
            # Processa em lotes para não sobrecarregar a API
            for i in range(0, total_documentos, self.batch_size):
                lote = documentos[i:i+self.batch_size]
                lote_processado = await self.processar_lote(lote, usuario_id)
                
                if lote_processado:
                    # Armazena o lote processado na Vector DB
                    sucesso = await self.armazenar_na_vector_db(lote_processado, usuario_id)
                    if sucesso:
                        documentos_processados += len(lote_processado)
                        
                # Pequena pausa para não sobrecarregar a API
                await asyncio.sleep(1)
            
            # Log do resultado
            logger.info(f"Processamento concluído: {documentos_processados}/{total_documentos} documentos")
            
            return (total_documentos, documentos_processados)
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao processar arquivo JSON: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao processar arquivo JSON: {str(e)}")
            return (0, 0)

    def generate_embeddings(self, documents: List[Dict[str, Any]]) -> List[List[float]]:
        """
        Gera embeddings para uma lista de documentos usando a API da OpenAI.
        
        Args:
            documents: Lista de documentos para gerar embeddings
            
        Returns:
            Lista de embeddings (vetores) para os documentos
        """
        try:
            # Extrai o texto dos documentos
            texts = [doc.get("conteudo", "") for doc in documents]
            
            # Gera embeddings em lotes
            all_embeddings = []
            for i in range(0, len(texts), self.batch_size):
                batch = texts[i:i + self.batch_size]
                
                # Chama a API da OpenAI para gerar embeddings
                response = self.client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=batch
                )
                
                # Extrai os embeddings da resposta
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)
            
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Erro ao gerar embeddings: {str(e)}")
            raise 
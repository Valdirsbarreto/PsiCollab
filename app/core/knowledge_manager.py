"""
Gerenciador da Base de Conhecimento do PsiCollab.
Responsável por criar, manter e atualizar a base de conhecimento para o RAG Engine.
"""
from typing import Dict, Any, List, Optional, Tuple
import os
import json
import asyncio
import logging
import uuid
from datetime import datetime
from app.core.embedding_generator import EmbeddingGenerator
from app.core.audit import AuditoriaManager, TipoOperacao, NivelSensibilidade
from app.core.config import settings
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configuração de logging
logger = logging.getLogger(__name__)

class KnowledgeManager:
    """
    Gerenciador da Base de Conhecimento do PsiCollab.
    Coordena a criação, manutenção e atualização da base de conhecimento
    que alimenta o RAG Engine.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de conhecimento."""
        self.knowledge_dir = settings.KNOWLEDGE_BASE_DIR
        self.embedding_generator = EmbeddingGenerator()
        self.audit_manager = AuditoriaManager()
        self.base_dir = Path(settings.KNOWLEDGE_BASE_DIR)
        self.client = QdrantClient(settings.VECTOR_DB_URL)
        
        # Verificar e criar diretório de conhecimento se não existir
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            
    async def inicializar_base_conhecimento(
        self,
        usuario_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inicializa a base de conhecimento, processando todos os arquivos JSON
        no diretório de conhecimento.
        
        Args:
            usuario_id: ID do usuário para auditoria
            
        Returns:
            Estatísticas do processamento
        """
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.INICIALIZACAO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="knowledge_base",
            detalhes={
                "operacao": "inicializar_base_conhecimento"
            }
        )
        
        try:
            # Lista todos os arquivos JSON no diretório
            arquivos_json = [
                os.path.join(self.knowledge_dir, arquivo)
                for arquivo in os.listdir(self.knowledge_dir)
                if arquivo.endswith('.json')
            ]
            
            if not arquivos_json:
                logger.warning("Nenhum arquivo JSON encontrado no diretório de conhecimento")
                return {
                    "status": "aviso",
                    "mensagem": "Nenhum arquivo JSON encontrado",
                    "arquivos_processados": 0,
                    "total_documentos": 0,
                    "documentos_processados": 0
                }
            
            # Estatísticas do processamento
            estatisticas = {
                "arquivos_processados": 0,
                "total_documentos": 0,
                "documentos_processados": 0
            }
            
            # Processa cada arquivo JSON
            for arquivo in arquivos_json:
                logger.info(f"Processando arquivo: {arquivo}")
                total, processados = await self.embedding_generator.processar_arquivo_json(
                    arquivo, usuario_id
                )
                
                estatisticas["arquivos_processados"] += 1
                estatisticas["total_documentos"] += total
                estatisticas["documentos_processados"] += processados
            
            # Calcula a taxa de sucesso
            if estatisticas["total_documentos"] > 0:
                taxa_sucesso = (estatisticas["documentos_processados"] / estatisticas["total_documentos"]) * 100
                estatisticas["taxa_sucesso"] = f"{taxa_sucesso:.2f}%"
            else:
                estatisticas["taxa_sucesso"] = "N/A"
            
            estatisticas["status"] = "sucesso"
            
            # Log das estatísticas
            logger.info(f"Inicialização da base de conhecimento concluída: {estatisticas}")
            
            return estatisticas
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao inicializar base de conhecimento: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao inicializar base de conhecimento: {str(e)}")
            return {
                "status": "erro",
                "mensagem": str(e),
                "arquivos_processados": 0,
                "total_documentos": 0,
                "documentos_processados": 0
            }
    
    async def adicionar_documento(
        self,
        documento: Dict[str, Any],
        usuario_id: Optional[str] = None
    ) -> bool:
        """
        Adiciona um novo documento à base de conhecimento.
        
        Args:
            documento: Documento a ser adicionado
            usuario_id: ID do usuário para auditoria
            
        Returns:
            True se o documento foi adicionado com sucesso, False caso contrário
        """
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.CRIACAO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="knowledge_base",
            detalhes={
                "operacao": "adicionar_documento",
                "documento_id": documento.get("id", "N/A"),
                "tipo": documento.get("tipo", "N/A")
            }
        )
        
        try:
            # Processa o documento
            documento_processado = await self.embedding_generator.processar_documento(
                documento, usuario_id
            )
            
            # Armazena na Vector DB
            sucesso = await self.embedding_generator.armazenar_na_vector_db(
                [documento_processado], usuario_id
            )
            
            # Atualiza o arquivo JSON correspondente
            if sucesso:
                await self._atualizar_arquivo_json(documento)
            
            return sucesso
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao adicionar documento: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao adicionar documento: {str(e)}")
            return False
    
    async def _atualizar_arquivo_json(self, documento: Dict[str, Any]) -> None:
        """
        Atualiza o arquivo JSON correspondente ao tipo do documento.
        
        Args:
            documento: Documento a ser adicionado ao arquivo JSON
        """
        # Determina o arquivo baseado no tipo do documento
        tipo_documento = documento.get("tipo", "geral")
        nome_arquivo = f"{tipo_documento.lower().replace(' ', '_')}.json"
        caminho_arquivo = os.path.join(self.knowledge_dir, nome_arquivo)
        
        try:
            # Carrega o arquivo se existir
            documentos = []
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    documentos = json.load(f)
            
            # Verifica se o documento já existe
            for i, doc in enumerate(documentos):
                if doc.get("id") == documento.get("id"):
                    # Atualiza o documento existente
                    documentos[i] = documento
                    break
            else:
                # Adiciona o novo documento
                documentos.append(documento)
            
            # Salva o arquivo atualizado
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(documentos, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Erro ao atualizar arquivo JSON {caminho_arquivo}: {str(e)}")
            raise
    
    async def criar_base_conhecimento_inicial(
        self,
        usuario_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cria a base de conhecimento inicial com documentos essenciais.
        
        Args:
            usuario_id: ID do usuário para auditoria
            
        Returns:
            Estatísticas da criação
        """
        # Registra a operação na auditoria
        registro = self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.CRIACAO,
            nivel_sensibilidade=NivelSensibilidade.MEDIO,
            usuario_id=usuario_id or "sistema",
            recurso="knowledge_base",
            detalhes={
                "operacao": "criar_base_conhecimento_inicial"
            }
        )
        
        try:
            # Categorias da base de conhecimento inicial
            categorias = [
                "wechsler",
                "personalidade",
                "atencao",
                "neuropsicologico",
                "projetivo",
                "desenvolvimento",
                "recomendacoes",
                "normativas",
                "etica"
            ]
            
            # Criar os arquivos JSON de exemplo para cada categoria
            for categoria in categorias:
                await self._criar_arquivo_exemplo(categoria)
            
            # Inicializar a base de conhecimento
            return await self.inicializar_base_conhecimento(usuario_id)
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                registro,
                f"Erro ao criar base de conhecimento inicial: {str(e)}"
            )
            # Log do erro
            logger.error(f"Erro ao criar base de conhecimento inicial: {str(e)}")
            return {
                "status": "erro",
                "mensagem": str(e)
            }
    
    async def _criar_arquivo_exemplo(self, categoria: str) -> None:
        """
        Cria um arquivo JSON de exemplo para uma categoria.
        
        Args:
            categoria: Nome da categoria
        """
        nome_arquivo = f"{categoria}.json"
        caminho_arquivo = os.path.join(self.knowledge_dir, nome_arquivo)
        
        # Verifica se o arquivo já existe
        if os.path.exists(caminho_arquivo):
            logger.info(f"Arquivo {nome_arquivo} já existe, pulando criação")
            return
        
        # Cria o conteúdo de exemplo baseado na categoria
        documentos = self._gerar_documentos_exemplo(categoria)
        
        # Salva o arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(documentos, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Arquivo {nome_arquivo} criado com {len(documentos)} documentos de exemplo")
    
    def _gerar_documentos_exemplo(self, categoria: str) -> List[Dict[str, Any]]:
        """
        Gera documentos de exemplo para uma categoria.
        
        Args:
            categoria: Nome da categoria
            
        Returns:
            Lista de documentos de exemplo
        """
        documentos = []
        
        if categoria == "wechsler":
            documentos = [
                {
                    "id": "wechsler_001",
                    "tipo": "wechsler",
                    "conteudo": "A Escala Wechsler de Inteligência para Crianças (WISC) avalia o funcionamento intelectual de crianças entre 6 e 16 anos. O QI Total é derivado dos índices de Compreensão Verbal, Raciocínio Perceptual, Memória Operacional e Velocidade de Processamento. Escores entre 90 e 109 são considerados na média. Escores acima de 130 indicam capacidade intelectual muito superior, enquanto escores abaixo de 70 podem indicar deficiência intelectual, embora múltiplos fatores devam ser considerados para esse diagnóstico.",
                    "metadata": {
                        "fonte": "Manual técnico WISC-IV",
                        "ano": 2013,
                        "relevancia": "alta",
                        "autor": "David Wechsler"
                    }
                },
                {
                    "id": "wechsler_002",
                    "tipo": "wechsler",
                    "conteudo": "O Índice de Compreensão Verbal (ICV) da escala Wechsler avalia a formação de conceitos verbais, raciocínio verbal e conhecimento adquirido. Escores baixos no ICV podem refletir dificuldades na compreensão verbal, vocabulário limitado ou baixa exposição a conteúdos educacionais. É importante considerar fatores culturais e educacionais na interpretação desses resultados, especialmente em contextos de vulnerabilidade socioeconômica.",
                    "metadata": {
                        "fonte": "Interpretação clínica das Escalas Wechsler",
                        "ano": 2019,
                        "relevancia": "alta",
                        "autor": "Silva, M.T."
                    }
                }
            ]
        elif categoria == "personalidade":
            documentos = [
                {
                    "id": "personalidade_001",
                    "tipo": "personalidade",
                    "conteudo": "O MMPI-2 (Inventário Multifásico de Personalidade Minnesota) é um dos instrumentos mais amplamente utilizados para avaliação de personalidade e psicopatologia. Contém escalas de validade que avaliam a abordagem do examinando ao teste. Elevações nas escalas clínicas podem sugerir diferentes configurações de personalidade ou condições psicopatológicas, mas devem ser interpretadas no contexto global da avaliação e história do indivíduo.",
                    "metadata": {
                        "fonte": "Manual do MMPI-2",
                        "ano": 2003,
                        "relevancia": "alta",
                        "autor": "Butcher, J.N."
                    }
                },
                {
                    "id": "personalidade_002",
                    "tipo": "personalidade",
                    "conteudo": "O Inventário de Personalidade NEO PI-R avalia os cinco grandes fatores de personalidade: Neuroticismo, Extroversão, Abertura, Amabilidade e Conscienciosidade. Cada fator é composto por seis facetas, permitindo uma avaliação abrangente e detalhada da personalidade normal. O instrumento é particularmente útil em contextos de orientação profissional, seleção de pessoal e compreensão de diferenças individuais em diversos contextos.",
                    "metadata": {
                        "fonte": "Manual técnico do NEO PI-R",
                        "ano": 2010,
                        "relevancia": "alta",
                        "autor": "Costa, P.T. & McCrae, R.R."
                    }
                }
            ]
        elif categoria == "atencao":
            documentos = [
                {
                    "id": "atencao_001",
                    "tipo": "atencao",
                    "conteudo": "O Teste D2 de Atenção Concentrada avalia a atenção seletiva e a capacidade de concentração. Fornece medidas de velocidade de processamento, precisão e consistência do desempenho. Escores baixos podem sugerir dificuldades atencionais, impulsividade ou problemas na capacidade de discriminação visual. É importante considerar fatores como ansiedade, fadiga e motivação na interpretação dos resultados.",
                    "metadata": {
                        "fonte": "Manual do Teste D2",
                        "ano": 2015,
                        "relevancia": "alta",
                        "autor": "Brickenkamp, R."
                    }
                },
                {
                    "id": "atencao_002",
                    "tipo": "atencao",
                    "conteudo": "O TEACO-FF (Teste de Atenção Concentrada) avalia a capacidade de selecionar estímulos em meio a distratores, mantendo o foco por determinado período. Resultados abaixo da média podem indicar dificuldades em sustentar a atenção, comprometendo tarefas que exigem vigilância ou foco prolongado. Em avaliações para TDAH, este teste deve ser complementado por outras medidas e informações clínicas.",
                    "metadata": {
                        "fonte": "Manual do TEACO-FF",
                        "ano": 2018,
                        "relevancia": "media",
                        "autor": "Rueda, F.J.M."
                    }
                }
            ]
        elif categoria == "normativas":
            documentos = [
                {
                    "id": "normativas_001",
                    "tipo": "normativas",
                    "conteudo": "De acordo com a Resolução CFP nº 06/2019, os documentos psicológicos devem ser fundamentados na observância dos princípios e dispositivos do Código de Ética Profissional do Psicólogo. A linguagem deve ser precisa, clara, inteligível e concisa, ou seja, deve-se restringir pontualmente às informações que se fizerem necessárias. O texto deve ser escrito em narrativa descritiva e precisa, ilustrado com fundamentos teóricos, baseado em dados colhidos e analisados à luz de um instrumental técnico.",
                    "metadata": {
                        "fonte": "Resolução CFP nº 06/2019",
                        "ano": 2019,
                        "relevancia": "alta",
                        "autor": "Conselho Federal de Psicologia"
                    }
                },
                {
                    "id": "normativas_002",
                    "tipo": "normativas",
                    "conteudo": "O laudo psicológico deve conter no mínimo: 1) identificação; 2) descrição da demanda; 3) procedimento; 4) análise; 5) conclusão. Na conclusão do documento, deve constar o posicionamento profissional após a exposição dos resultados obtidos e das considerações realizadas, respondendo à demanda inicial. É facultado ao psicólogo acrescentar outros itens ao documento, desde que não prejudiquem a clareza e objetividade da comunicação.",
                    "metadata": {
                        "fonte": "Resolução CFP nº 06/2019",
                        "ano": 2019,
                        "relevancia": "alta",
                        "autor": "Conselho Federal de Psicologia"
                    }
                }
            ]
        elif categoria == "etica":
            documentos = [
                {
                    "id": "etica_001",
                    "tipo": "etica",
                    "conteudo": "O Código de Ética Profissional do Psicólogo estabelece que o profissional deve basear seu trabalho no respeito e na promoção da liberdade, dignidade, igualdade e integridade do ser humano, apoiado nos valores que embasam a Declaração Universal dos Direitos Humanos. O psicólogo deve atuar com responsabilidade social, analisando crítica e historicamente a realidade política, econômica, social e cultural.",
                    "metadata": {
                        "fonte": "Código de Ética Profissional do Psicólogo",
                        "ano": 2005,
                        "relevancia": "alta",
                        "autor": "Conselho Federal de Psicologia"
                    }
                },
                {
                    "id": "etica_002",
                    "tipo": "etica",
                    "conteudo": "Na utilização de instrumentos e procedimentos de avaliação psicológica, o psicólogo deve considerar as limitações das técnicas, os padrões psicométricos e a validade dos instrumentos para os diferentes contextos e populações. É fundamental considerar aspectos culturais, sociais e econômicos na interpretação dos resultados, evitando generalizações indevidas e discriminações.",
                    "metadata": {
                        "fonte": "Código de Ética Profissional do Psicólogo",
                        "ano": 2005,
                        "relevancia": "alta",
                        "autor": "Conselho Federal de Psicologia"
                    }
                }
            ]
        
        return documentos

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
        Armazena documentos e seus embeddings na Vector DB.
        
        Args:
            documents: Lista de documentos
            embeddings: Lista de embeddings correspondentes
        """
        try:
            # Cria a coleção se não existir
            collection_name = "knowledge_base"
            try:
                self.client.get_collection(collection_name)
            except:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Tamanho dos vetores do modelo text-embedding-ada-002
                        distance=models.Distance.COSINE
                    )
                )

            # Prepara os pontos para inserção
            points = []
            for doc, emb in zip(documents, embeddings):
                # Gera um UUID para cada ponto
                point_id = str(uuid.uuid4())
                points.append(
                    models.PointStruct(
                        id=point_id,  # Usa UUID como ID
                        vector=emb,
                        payload=doc
                    )
                )

            # Insere os pontos na coleção
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )

            logger.info(f"Armazenados {len(documents)} documentos na Vector DB")

        except Exception as e:
            logger.error(f"Erro ao armazenar documentos: {str(e)}")
            raise 
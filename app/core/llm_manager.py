"""
Gerenciador de Modelos de Linguagem para interpretação de testes psicológicos.
"""
from typing import Dict, Any, List, Optional
import openai
from datetime import datetime
from app.core.config import settings
from app.core.audit import (
    AuditoriaManager,
    TipoOperacao,
    NivelSensibilidade,
    RegistroAuditoria
)
from app.core.rag_engine import RAGEngine
import json

class LLMManager:
    """
    Gerenciador de Modelos de Linguagem para processamento e interpretação
    de resultados de testes psicológicos.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de LLM."""
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        
        # Configura o cliente OpenAI
        openai.api_key = self.api_key
        
        # Inicializa o gerenciador de auditoria
        self.audit_manager = AuditoriaManager()
        
        # Inicializa o motor RAG
        self.rag_engine = RAGEngine()
        
        # Templates para diferentes tipos de interpretação
        self.templates = {
            "wechsler": """
            Analise os seguintes resultados do teste de inteligência {test_type}:
            
            Nível Intelectual: {nivel_intelectual}
            Perfil Cognitivo: {perfil_cognitivo}
            Pontos Fortes: {pontos_fortes}
            Pontos de Atenção: {pontos_fracos}
            
            Forneça uma interpretação detalhada considerando:
            1. Capacidades cognitivas gerais
            2. Forças e limitações específicas
            3. Implicações para o desenvolvimento/acadêmico
            4. Recomendações para intervenção
            """,
            
            "personality": """
            Analise os seguintes resultados do teste de personalidade {test_type}:
            
            Validade: {validade}
            Perfil de Personalidade: {perfil_personalidade}
            Características Principais: {caracteristicas_principais}
            Pontos de Atenção: {pontos_atencao}
            
            Forneça uma interpretação detalhada considerando:
            1. Padrões de personalidade
            2. Fatores de risco e proteção
            3. Implicações para o funcionamento social
            4. Recomendações para desenvolvimento pessoal
            """,
            
            "projective": """
            Analise os seguintes resultados do teste projetivo {test_type}:
            
            Validade: {validade}
            Perfil de Personalidade: {perfil_personalidade}
            Características Principais: {caracteristicas_principais}
            Pontos de Atenção: {pontos_atencao}
            
            Forneça uma interpretação detalhada considerando:
            1. Dinâmicas psicológicas subjacentes
            2. Padrões de funcionamento emocional
            3. Implicações para o desenvolvimento
            4. Recomendações para intervenção psicológica
            """
        }
    
    def _registrar_operacao_llm(
        self,
        tipo_operacao: str,
        test_type: str,
        usuario_id: str,
        detalhes: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> RegistroAuditoria:
        """
        Registra uma operação do LLM na auditoria.
        
        Args:
            tipo_operacao: Tipo da operação
            test_type: Tipo do teste
            usuario_id: ID do usuário
            detalhes: Detalhes da operação
            ip_address: Endereço IP
            user_agent: User Agent
            
        Returns:
            RegistroAuditoria: Registro da operação
        """
        return self.audit_manager.registrar_operacao(
            tipo_operacao=TipoOperacao.PROCESSAMENTO,
            nivel_sensibilidade=NivelSensibilidade.ALTO,
            usuario_id=usuario_id,
            recurso=f"llm_{test_type}",
            detalhes={
                "tipo_operacao": tipo_operacao,
                "test_type": test_type,
                **detalhes
            },
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    async def gerar_interpretacao_avancada(
        self,
        test_type: str,
        resultados: Dict[str, Any],
        usuario_id: str,
        contexto: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gera uma interpretação avançada dos resultados usando LLM.
        
        Args:
            test_type: Tipo do teste (wechsler, personality, projective)
            resultados: Dicionário com os resultados do teste
            usuario_id: ID do usuário que solicitou a interpretação
            contexto: Dicionário opcional com informações adicionais
            ip_address: Endereço IP do usuário
            user_agent: User Agent do navegador
            
        Returns:
            Dict com a interpretação avançada
        """
        # Valida o tipo de teste
        if test_type not in self.templates:
            raise ValueError(f"Tipo de teste não suportado: {test_type}")
        
        # Registra início da operação
        self._registro_atual = self._registrar_operacao_llm(
            "interpretacao_avancada",
            test_type,
            usuario_id,
            {"resultados": resultados},
            ip_address,
            user_agent
        )
        
        try:
            # Prepara o prompt base com base no template
            prompt_base = self.templates[test_type].format(**resultados)
            
            # Adiciona contexto se fornecido
            if contexto:
                prompt_base += "\n\nContexto Adicional:\n"
                for key, value in contexto.items():
                    prompt_base += f"{key}: {value}\n"
            
            # Busca conhecimento específico usando o RAG
            conhecimento = await self.rag_engine.buscar_conhecimento(
                test_type=test_type,
                contexto={**resultados, **(contexto or {})},
                usuario_id=usuario_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Enriquece o prompt com conhecimento específico
            prompt_enriquecido = self.rag_engine.enriquecer_prompt(
                prompt_base,
                conhecimento
            )
            
            # Gera a interpretação usando o LLM
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um psicólogo especializado em interpretação de testes psicológicos."},
                    {"role": "user", "content": prompt_enriquecido}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Processa a resposta
            interpretacao = response.choices[0].message.content
            
            # Estrutura o resultado
            resultado = {
                "test_type": test_type,
                "data_interpretacao": datetime.now().isoformat(),
                "interpretacao": interpretacao,
                "modelo_utilizado": self.model,
                "parametros": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                "conhecimento_utilizado": [
                    {
                        "conteudo": doc["conteudo"],
                        "fonte": doc["metadata"].get("fonte", "N/A"),
                        "ano": doc["metadata"].get("ano", "N/A")
                    }
                    for doc in conhecimento
                ]
            }
            
            # Adiciona contexto se fornecido
            if contexto:
                resultado["contexto"] = contexto
            
            return resultado
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                self._registro_atual,
                f"Erro ao gerar interpretação: {str(e)}"
            )
            raise
    
    async def gerar_recomendacoes_personalizadas(
        self,
        test_type: str,
        resultados: Dict[str, Any],
        usuario_id: str,
        contexto: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> List[str]:
        """
        Gera recomendações personalizadas baseadas nos resultados.
        
        Args:
            test_type: Tipo do teste
            resultados: Dicionário com os resultados
            usuario_id: ID do usuário
            contexto: Dicionário opcional com informações adicionais
            ip_address: Endereço IP do usuário
            user_agent: User Agent do navegador
            
        Returns:
            Lista de recomendações
        """
        # Registra início da operação
        self._registro_atual = self._registrar_operacao_llm(
            "recomendacoes",
            test_type,
            usuario_id,
            {"resultados": resultados},
            ip_address,
            user_agent
        )
        
        try:
            # Prepara o prompt base
            prompt_base = f"""
            Com base nos seguintes resultados do teste {test_type}:
            {json.dumps(resultados, ensure_ascii=False, indent=2)}
            
            Gere 5 recomendações específicas e acionáveis para:
            1. Desenvolvimento pessoal/profissional
            2. Intervenções psicológicas
            3. Acomodações educacionais (se aplicável)
            4. Suporte familiar/social
            5. Acompanhamento profissional
            """
            
            if contexto:
                prompt_base += f"\n\nContexto Adicional:\n{json.dumps(contexto, ensure_ascii=False, indent=2)}"
            
            # Busca conhecimento específico usando o RAG
            conhecimento = await self.rag_engine.buscar_conhecimento(
                test_type=test_type,
                contexto={**resultados, **(contexto or {})},
                usuario_id=usuario_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Enriquece o prompt com conhecimento específico
            prompt_enriquecido = self.rag_engine.enriquecer_prompt(
                prompt_base,
                conhecimento
            )
            
            # Gera as recomendações usando o LLM
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um psicólogo especializado em desenvolvimento e intervenção."},
                    {"role": "user", "content": prompt_enriquecido}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Processa e estrutura as recomendações
            recomendacoes = response.choices[0].message.content.split("\n")
            recomendacoes = [r.strip() for r in recomendacoes if r.strip()]
            
            return recomendacoes[:5]  # Limita a 5 recomendações
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                self._registro_atual,
                f"Erro ao gerar recomendações: {str(e)}"
            )
            raise
    
    async def gerar_relatorio_completo(
        self,
        test_type: str,
        resultados: Dict[str, Any],
        usuario_id: str,
        contexto: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Gera um relatório completo integrando resultados e interpretações.
        
        Args:
            test_type: Tipo do teste
            resultados: Dicionário com os resultados
            usuario_id: ID do usuário
            contexto: Dicionário opcional com informações adicionais
            ip_address: Endereço IP do usuário
            user_agent: User Agent do navegador
            
        Returns:
            Dict com o relatório completo
        """
        # Registra início da operação
        self._registro_atual = self._registrar_operacao_llm(
            "relatorio_completo",
            test_type,
            usuario_id,
            {"resultados": resultados},
            ip_address,
            user_agent
        )
        
        try:
            # Gera interpretação avançada
            interpretacao = await self.gerar_interpretacao_avancada(
                test_type, resultados, usuario_id, contexto, ip_address, user_agent
            )
            
            # Gera recomendações personalizadas
            recomendacoes = await self.gerar_recomendacoes_personalizadas(
                test_type, resultados, usuario_id, contexto, ip_address, user_agent
            )
            
            # Estrutura o relatório completo
            relatorio = {
                "test_type": test_type,
                "data_geracao": datetime.now().isoformat(),
                "resultados_brutos": resultados,
                "interpretacao_avancada": interpretacao,
                "recomendacoes_personalizadas": recomendacoes,
                "modelo_utilizado": self.model
            }
            
            if contexto:
                relatorio["contexto"] = contexto
            
            return relatorio
            
        except Exception as e:
            # Registra o erro na auditoria
            self.audit_manager.registrar_erro(
                self._registro_atual,
                f"Erro ao gerar relatório: {str(e)}"
            )
            raise 
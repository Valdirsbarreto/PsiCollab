from typing import Dict, Any, List
from .base_processor import BaseTestProcessor

class ProjectiveProcessor(BaseTestProcessor):
    """
    Processador para testes projetivos (Rorschach, TAT, etc.).
    """
    
    def __init__(self, test_type: str = "Rorschach"):
        super().__init__()
        self.test_type = test_type
        self.version = "1.0"  # Versão padrão
        
        # Configurações específicas por tipo de teste
        self.config = {
            "Rorschach": {
                "laminas": list(range(1, 11)),
                "categorias": [
                    "Localização",
                    "Determinantes",
                    "Conteúdo",
                    "Qualidade Formal",
                    "Qualidade Popular",
                    "Respostas Organizadas"
                ],
                "normas": {
                    "media_respostas": 20,
                    "desvio_padrao": 5
                }
            },
            "TAT": {
                "laminas": list(range(1, 21)),
                "categorias": [
                    "Tema Principal",
                    "Herói",
                    "Necessidades",
                    "Pressões",
                    "Conflitos",
                    "Outcome"
                ],
                "normas": {
                    "media_histórias": 10,
                    "desvio_padrao": 2
                }
            }
        }
        
        # Validação do tipo de teste
        if test_type not in self.config:
            raise ValueError(f"Tipo de teste não suportado: {test_type}")
    
    def processar_dados(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados brutos do teste projetivo.
        """
        if not self._validar_dados_projetivo(dados):
            raise ValueError(f"Dados do teste {self.test_type} inválidos")
        
        dados_processados = {
            "respostas": {},
            "tempos": {},
            "observacoes": {},
            "comportamento": {}
        }
        
        # Processa respostas por lâmina
        for lamina in self.config[self.test_type]["laminas"]:
            if str(lamina) in dados:
                dados_processados["respostas"][lamina] = {
                    "conteudo": dados[str(lamina)]["conteudo"],
                    "localizacao": dados[str(lamina)].get("localizacao", ""),
                    "determinantes": dados[str(lamina)].get("determinantes", []),
                    "tempo": dados[str(lamina)].get("tempo", 0)
                }
        
        # Processa observações comportamentais
        if "comportamento" in dados:
            dados_processados["comportamento"] = dados["comportamento"]
        
        # Processa observações gerais
        if "observacoes" in dados:
            dados_processados["observacoes"] = dados["observacoes"]
        
        return dados_processados
    
    def calcular_escores(self, dados_processados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula os escores do teste projetivo.
        """
        escores = {
            "respostas": {},
            "indices": {},
            "perfil": {}
        }
        
        # Calcula escores por lâmina
        for lamina, dados in dados_processados["respostas"].items():
            escores["respostas"][lamina] = {
                "qualidade_formal": self._avaliar_qualidade_formal(dados),
                "qualidade_popular": self._avaliar_qualidade_popular(dados),
                "organizacao": self._avaliar_organizacao(dados)
            }
        
        # Calcula índices globais
        escores["indices"] = self._calcular_indices(escores["respostas"])
        
        # Calcula perfil
        escores["perfil"] = self._calcular_perfil(escores["indices"])
        
        return escores
    
    def interpretar_resultados(self, escores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpreta os resultados do teste projetivo.
        """
        interpretacao = {
            "validade": self._avaliar_validade(escores),
            "perfil_personalidade": self._interpretar_perfil(escores["perfil"]),
            "caracteristicas_principais": [],
            "pontos_atencao": [],
            "recomendacoes": []
        }
        
        # Analisa características principais
        for indice, valor in escores["indices"].items():
            if valor > 1.5:
                interpretacao["caracteristicas_principais"].append(
                    f"Elevado em {indice}"
                )
            elif valor < 0.5:
                interpretacao["pontos_atencao"].append(
                    f"Baixo em {indice}"
                )
        
        # Gera recomendações
        interpretacao["recomendacoes"] = self._gerar_recomendacoes(
            interpretacao["perfil_personalidade"],
            interpretacao["caracteristicas_principais"],
            interpretacao["pontos_atencao"]
        )
        
        return interpretacao
    
    def gerar_relatorio(self, interpretacao: Dict[str, Any]) -> str:
        """
        Gera um relatório estruturado dos resultados do teste projetivo.
        """
        relatorio = f"""
        RELATÓRIO DE AVALIAÇÃO - {self.test_type}
        
        1. Validade do Teste
        {interpretacao['validade']}
        
        2. Perfil de Personalidade
        {interpretacao['perfil_personalidade']}
        
        3. Características Principais
        {', '.join(interpretacao['caracteristicas_principais'])}
        
        4. Pontos de Atenção
        {', '.join(interpretacao['pontos_atencao'])}
        
        5. Recomendações
        {chr(10).join(interpretacao['recomendacoes'])}
        """
        
        return relatorio
    
    def _validar_dados_projetivo(self, dados: Dict[str, Any]) -> bool:
        """
        Validação específica para dados do teste projetivo.
        """
        if not dados or not isinstance(dados, dict):
            return False
        
        # Verifica se há respostas para pelo menos algumas lâminas
        respostas_validas = 0
        for lamina in self.config[self.test_type]["laminas"]:
            if str(lamina) in dados:
                respostas_validas += 1
        
        return respostas_validas >= len(self.config[self.test_type]["laminas"]) * 0.7
    
    def _avaliar_qualidade_formal(self, dados: Dict[str, Any]) -> float:
        """
        Avalia a qualidade formal da resposta.
        """
        # Implementar avaliação específica
        return 1.0
    
    def _avaliar_qualidade_popular(self, dados: Dict[str, Any]) -> float:
        """
        Avalia a qualidade popular da resposta.
        """
        # Implementar avaliação específica
        return 1.0
    
    def _avaliar_organizacao(self, dados: Dict[str, Any]) -> float:
        """
        Avalia a organização da resposta.
        """
        # Implementar avaliação específica
        return 1.0
    
    def _calcular_indices(self, respostas: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula os índices globais do teste.
        """
        # Implementar cálculo específico
        return {}
    
    def _calcular_perfil(self, indices: Dict[str, float]) -> Dict[str, Any]:
        """
        Calcula o perfil baseado nos índices.
        """
        # Implementar cálculo específico
        return {}
    
    def _avaliar_validade(self, escores: Dict[str, Any]) -> str:
        """
        Avalia a validade dos resultados do teste.
        """
        # Implementar avaliação específica
        return "Resultados válidos"
    
    def _interpretar_perfil(self, perfil: Dict[str, Any]) -> str:
        """
        Interpreta o perfil de personalidade.
        """
        # Implementar interpretação específica
        return "Perfil interpretado"
    
    def _gerar_recomendacoes(self, perfil: str, caracteristicas: List[str],
                           pontos_atencao: List[str]) -> List[str]:
        """
        Gera recomendações baseadas no perfil.
        """
        recomendacoes = []
        
        # Adiciona recomendações baseadas nas características
        for caracteristica in caracteristicas:
            recomendacoes.append(
                f"Considerar intervenções que aproveitem a característica de {caracteristica}"
            )
        
        # Adiciona recomendações baseadas nos pontos de atenção
        for ponto in pontos_atencao:
            recomendacoes.append(
                f"Desenvolver estratégias para trabalhar {ponto}"
            )
        
        return recomendacoes 
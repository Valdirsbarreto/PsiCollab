from typing import Dict, Any, List
from .base_processor import BaseTestProcessor

class PersonalityProcessor(BaseTestProcessor):
    """
    Processador para testes de personalidade (MMPI, NEO-PI-R, etc.).
    """
    
    def __init__(self, test_type: str = "MMPI-2"):
        super().__init__()
        self.test_type = test_type
        self.version = "2.0"  # Versão padrão
        
        # Configurações específicas por tipo de teste
        self.config = {
            "MMPI-2": {
                "escalas": [
                    "Hipocondria",
                    "Depressão",
                    "Histeria",
                    "Desvio Psicopático",
                    "Masculinidade/Feminilidade",
                    "Paranóia",
                    "Psicastenia",
                    "Esquizofrenia",
                    "Hipomania",
                    "Introversão Social"
                ],
                "normas": {
                    "media": 50,
                    "desvio_padrao": 10
                }
            },
            "NEO-PI-R": {
                "escalas": [
                    "Neuroticismo",
                    "Extroversão",
                    "Abertura",
                    "Agradabilidade",
                    "Conscienciosidade"
                ],
                "normas": {
                    "media": 50,
                    "desvio_padrao": 10
                }
            }
        }
        
        # Validação do tipo de teste
        if test_type not in self.config:
            raise ValueError(f"Tipo de teste não suportado: {test_type}")
    
    def processar_dados(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados brutos do teste de personalidade.
        """
        if not self._validar_dados_personalidade(dados):
            raise ValueError(f"Dados do teste {self.test_type} inválidos")
        
        dados_processados = {
            "escalas": {},
            "escores_validacao": {},
            "observacoes": {}
        }
        
        # Processa cada escala
        for escala in self.config[self.test_type]["escalas"]:
            if escala in dados:
                dados_processados["escalas"][escala] = {
                    "escore_bruto": dados[escala]["escore_bruto"],
                    "respostas": dados[escala].get("respostas", []),
                    "tempo": dados[escala].get("tempo", 0)
                }
        
        # Processa escores de validação
        if "validacao" in dados:
            dados_processados["escores_validacao"] = dados["validacao"]
        
        # Processa observações
        if "observacoes" in dados:
            dados_processados["observacoes"] = dados["observacoes"]
        
        return dados_processados
    
    def calcular_escores(self, dados_processados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula os escores do teste de personalidade.
        """
        escores = {
            "escalas": {},
            "escores_validacao": {},
            "perfil": {}
        }
        
        # Calcula escores das escalas
        for escala, dados in dados_processados["escalas"].items():
            escores["escalas"][escala] = {
                "escore_padronizado": self._calcular_escore_padronizado(
                    dados["escore_bruto"],
                    self.config[self.test_type]["normas"]
                )
            }
        
        # Processa escores de validação
        escores["escores_validacao"] = self._processar_validacao(
            dados_processados["escores_validacao"]
        )
        
        # Calcula perfil
        escores["perfil"] = self._calcular_perfil(escores["escalas"])
        
        return escores
    
    def interpretar_resultados(self, escores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpreta os resultados do teste de personalidade.
        """
        interpretacao = {
            "validade": self._avaliar_validade(escores["escores_validacao"]),
            "perfil_personalidade": self._interpretar_perfil(escores["perfil"]),
            "caracteristicas_principais": [],
            "pontos_atencao": [],
            "recomendacoes": []
        }
        
        # Analisa características principais
        for escala, escore in escores["escalas"].items():
            if escore["escore_padronizado"] > 65:
                interpretacao["caracteristicas_principais"].append(
                    f"Elevado em {escala}"
                )
            elif escore["escore_padronizado"] < 35:
                interpretacao["pontos_atencao"].append(
                    f"Baixo em {escala}"
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
        Gera um relatório estruturado dos resultados do teste de personalidade.
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
    
    def _validar_dados_personalidade(self, dados: Dict[str, Any]) -> bool:
        """
        Validação específica para dados do teste de personalidade.
        """
        if not dados or not isinstance(dados, dict):
            return False
        
        # Verifica se todas as escalas necessárias estão presentes
        for escala in self.config[self.test_type]["escalas"]:
            if escala not in dados:
                return False
        
        return True
    
    def _calcular_escore_padronizado(self, escore_bruto: float, 
                                   normas: Dict[str, float]) -> float:
        """
        Calcula o escore padronizado baseado nas normas.
        """
        return (escore_bruto - normas["media"]) / normas["desvio_padrao"]
    
    def _processar_validacao(self, dados_validacao: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os escores de validação do teste.
        """
        # Implementar processamento específico de validação
        return {}
    
    def _calcular_perfil(self, escores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula o perfil de personalidade baseado nos escores.
        """
        # Implementar cálculo específico do perfil
        return {}
    
    def _avaliar_validade(self, escores_validacao: Dict[str, Any]) -> str:
        """
        Avalia a validade dos resultados do teste.
        """
        # Implementar avaliação de validade
        return "Resultados válidos"
    
    def _interpretar_perfil(self, perfil: Dict[str, Any]) -> str:
        """
        Interpreta o perfil de personalidade.
        """
        # Implementar interpretação do perfil
        return "Perfil interpretado"
    
    def _gerar_recomendacoes(self, perfil: str, caracteristicas: List[str],
                           pontos_atencao: List[str]) -> List[str]:
        """
        Gera recomendações baseadas no perfil de personalidade.
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
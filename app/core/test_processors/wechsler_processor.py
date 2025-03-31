from typing import Dict, Any, List
from .base_processor import BaseTestProcessor

class WechslerProcessor(BaseTestProcessor):
    """
    Processador para testes de inteligência de Wechsler (WAIS, WISC, WPPSI).
    """
    
    def __init__(self, version: str = "WAIS-IV"):
        super().__init__()
        self.test_type = "Wechsler"
        self.version = version
        self.subtestes = {
            "WAIS-IV": [
                "Compreensão Verbal",
                "Raciocínio Perceptivo",
                "Memória de Trabalho",
                "Velocidade de Processamento"
            ],
            "WISC-IV": [
                "Compreensão Verbal",
                "Raciocínio Perceptivo",
                "Memória de Trabalho",
                "Velocidade de Processamento"
            ],
            "WPPSI-IV": [
                "Compreensão Verbal",
                "Raciocínio Visual",
                "Memória de Trabalho",
                "Velocidade de Processamento"
            ]
        }
        
        # Normas padrão (exemplo)
        self.normas = {
            "escore_bruto": {
                "media": 10,
                "desvio_padrao": 3
            },
            "escore_total": {
                "media": 100,
                "desvio_padrao": 15
            }
        }
    
    def processar_dados(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados brutos do teste de Wechsler.
        """
        if not self._validar_dados_wechsler(dados):
            raise ValueError("Dados do teste de Wechsler inválidos")
        
        dados_processados = {
            "subtestes": {},
            "escores_compostos": {},
            "escore_total": 0
        }
        
        # Processa cada subteste
        for subteste in self.subtestes[self.version]:
            if subteste in dados:
                dados_processados["subtestes"][subteste] = {
                    "escore_bruto": dados[subteste]["escore_bruto"],
                    "tempo": dados[subteste].get("tempo", 0),
                    "observacoes": dados[subteste].get("observacoes", "")
                }
        
        return dados_processados
    
    def calcular_escores(self, dados_processados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula os escores do teste de Wechsler.
        """
        escores = {
            "subtestes": {},
            "escores_compostos": {},
            "escore_total": 0
        }
        
        # Calcula escores dos subtestes
        for subteste, dados in dados_processados["subtestes"].items():
            escores["subtestes"][subteste] = {
                "escore_padronizado": self._calcular_escore_padronizado(
                    dados["escore_bruto"],
                    self.normas["escore_bruto"]
                )
            }
        
        # Calcula escores compostos
        for indice in self.subtestes[self.version]:
            if indice in escores["subtestes"]:
                escores["escores_compostos"][indice] = self._calcular_escore_composto(
                    [escores["subtestes"][st]["escore_padronizado"] 
                     for st in self._get_subtestes_indice(indice)]
                )
        
        # Calcula escore total
        escores["escore_total"] = self._calcular_escore_total(
            escores["escores_compostos"]
        )
        
        return escores
    
    def interpretar_resultados(self, escores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpreta os resultados do teste de Wechsler.
        """
        interpretacao = {
            "nivel_intelectual": self._determinar_nivel_intelectual(
                escores["escore_total"]
            ),
            "perfil_cognitivo": self._analisar_perfil_cognitivo(
                escores["escores_compostos"]
            ),
            "pontos_fortes": [],
            "pontos_fracos": [],
            "recomendacoes": []
        }
        
        # Analisa pontos fortes e fracos
        for indice, escore in escores["escores_compostos"].items():
            if escore > 110:
                interpretacao["pontos_fortes"].append(indice)
            elif escore < 90:
                interpretacao["pontos_fracos"].append(indice)
        
        # Gera recomendações baseadas no perfil
        interpretacao["recomendacoes"] = self._gerar_recomendacoes(
            interpretacao["perfil_cognitivo"],
            interpretacao["pontos_fortes"],
            interpretacao["pontos_fracos"]
        )
        
        return interpretacao
    
    def gerar_relatorio(self, interpretacao: Dict[str, Any]) -> str:
        """
        Gera um relatório estruturado dos resultados do teste de Wechsler.
        """
        relatorio = f"""
        RELATÓRIO DE AVALIAÇÃO - {self.test_type} {self.version}
        
        1. Nível Intelectual
        {interpretacao['nivel_intelectual']}
        
        2. Perfil Cognitivo
        {interpretacao['perfil_cognitivo']}
        
        3. Pontos Fortes
        {', '.join(interpretacao['pontos_fortes'])}
        
        4. Pontos de Atenção
        {', '.join(interpretacao['pontos_fracos'])}
        
        5. Recomendações
        {chr(10).join(interpretacao['recomendacoes'])}
        """
        
        return relatorio
    
    def _validar_dados_wechsler(self, dados: Dict[str, Any]) -> bool:
        """
        Validação específica para dados do teste de Wechsler.
        """
        if not dados or not isinstance(dados, dict):
            return False
        
        # Verifica se todos os subtestes necessários estão presentes
        for subteste in self.subtestes[self.version]:
            if subteste not in dados:
                return False
        
        return True
    
    def _calcular_escore_padronizado(self, escore_bruto: float, normas: Dict[str, float]) -> float:
        """
        Calcula o escore padronizado baseado nas normas.
        """
        return (escore_bruto - normas["media"]) / normas["desvio_padrao"]
    
    def _calcular_escore_composto(self, escores: List[float]) -> float:
        """
        Calcula o escore composto de um índice.
        """
        return sum(escores) / len(escores)
    
    def _calcular_escore_total(self, escores_compostos: Dict[str, float]) -> float:
        """
        Calcula o escore total do teste.
        """
        return sum(escores_compostos.values()) / len(escores_compostos)
    
    def _determinar_nivel_intelectual(self, escore_total: float) -> str:
        """
        Determina o nível intelectual baseado no escore total.
        """
        if escore_total >= 130:
            return "Superior"
        elif escore_total >= 120:
            return "Acima da Média"
        elif escore_total >= 110:
            return "Média Superior"
        elif escore_total >= 90:
            return "Média"
        elif escore_total >= 80:
            return "Média Inferior"
        elif escore_total >= 70:
            return "Abaixo da Média"
        else:
            return "Inferior"
    
    def _analisar_perfil_cognitivo(self, escores_compostos: Dict[str, float]) -> str:
        """
        Analisa o perfil cognitivo baseado nos escores compostos.
        """
        # Implementar análise específica do perfil
        return "Perfil cognitivo analisado"
    
    def _get_subtestes_indice(self, indice: str) -> List[str]:
        """
        Retorna os subtestes que compõem um índice específico.
        """
        # Implementar mapeamento de subtestes por índice
        return []
    
    def _gerar_recomendacoes(self, perfil: str, pontos_fortes: List[str], 
                           pontos_fracos: List[str]) -> List[str]:
        """
        Gera recomendações baseadas no perfil cognitivo.
        """
        recomendacoes = []
        
        # Adiciona recomendações baseadas nos pontos fortes
        for ponto in pontos_fortes:
            recomendacoes.append(f"Utilizar estratégias que aproveitem a força em {ponto}")
        
        # Adiciona recomendações baseadas nos pontos fracos
        for ponto in pontos_fracos:
            recomendacoes.append(f"Desenvolver estratégias de compensação para {ponto}")
        
        return recomendacoes 
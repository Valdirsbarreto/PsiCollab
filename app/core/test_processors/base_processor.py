from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class BaseTestProcessor(ABC):
    """
    Classe base abstrata para processadores de testes psicológicos.
    Define a interface comum que todos os processadores devem implementar.
    """
    
    def __init__(self):
        self.test_type: str = ""
        self.version: str = ""
        self.normas: Dict[str, Any] = {}
        self.resultados: Dict[str, Any] = {}
        self.interpretacao: Dict[str, Any] = {}
        self.data_processamento: Optional[datetime] = None
    
    @abstractmethod
    def processar_dados(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados brutos do teste.
        
        Args:
            dados: Dicionário com os dados brutos do teste
            
        Returns:
            Dict com os resultados processados
        """
        pass
    
    @abstractmethod
    def calcular_escores(self, dados_processados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula os escores do teste.
        
        Args:
            dados_processados: Dados já processados do teste
            
        Returns:
            Dict com os escores calculados
        """
        pass
    
    @abstractmethod
    def interpretar_resultados(self, escores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpreta os resultados do teste.
        
        Args:
            escores: Dicionário com os escores calculados
            
        Returns:
            Dict com a interpretação dos resultados
        """
        pass
    
    @abstractmethod
    def gerar_relatorio(self, interpretacao: Dict[str, Any]) -> str:
        """
        Gera um relatório estruturado dos resultados.
        
        Args:
            interpretacao: Dicionário com a interpretação dos resultados
            
        Returns:
            String com o relatório formatado
        """
        pass
    
    def validar_dados(self, dados: Dict[str, Any]) -> bool:
        """
        Valida se os dados do teste estão completos e corretos.
        
        Args:
            dados: Dicionário com os dados do teste
            
        Returns:
            bool indicando se os dados são válidos
        """
        # Implementação padrão - pode ser sobrescrita
        return bool(dados and isinstance(dados, dict))
    
    def aplicar_normas(self, escores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica as normas do teste aos escores.
        
        Args:
            escores: Dicionário com os escores brutos
            
        Returns:
            Dict com os escores normalizados
        """
        # Implementação padrão - pode ser sobrescrita
        return escores
    
    def processar_teste(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o processamento completo do teste.
        
        Args:
            dados: Dicionário com os dados brutos do teste
            
        Returns:
            Dict com todos os resultados do processamento
        """
        if not self.validar_dados(dados):
            raise ValueError("Dados do teste inválidos")
        
        # Processa os dados
        dados_processados = self.processar_dados(dados)
        
        # Calcula os escores
        escores = self.calcular_escores(dados_processados)
        
        # Aplica as normas
        escores_normalizados = self.aplicar_normas(escores)
        
        # Interpreta os resultados
        interpretacao = self.interpretar_resultados(escores_normalizados)
        
        # Gera o relatório
        relatorio = self.gerar_relatorio(interpretacao)
        
        # Atualiza os atributos da classe
        self.resultados = escores_normalizados
        self.interpretacao = interpretacao
        self.data_processamento = datetime.now()
        
        return {
            "test_type": self.test_type,
            "version": self.version,
            "data_processamento": self.data_processamento.isoformat(),
            "resultados": self.resultados,
            "interpretacao": self.interpretacao,
            "relatorio": relatorio
        } 
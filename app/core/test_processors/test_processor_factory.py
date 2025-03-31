from typing import Dict, Type, List
from .base_processor import BaseTestProcessor
from .wechsler_processor import WechslerProcessor
from .personality_processor import PersonalityProcessor
from .projective_processor import ProjectiveProcessor

class TestProcessorFactory:
    """
    Factory para criar processadores de testes psicológicos.
    """
    
    _processors: Dict[str, Type[BaseTestProcessor]] = {
        "wechsler": WechslerProcessor,
        "personality": PersonalityProcessor,
        "projective": ProjectiveProcessor
    }
    
    @classmethod
    def create_processor(cls, test_type: str, **kwargs) -> BaseTestProcessor:
        """
        Cria um processador específico para o tipo de teste solicitado.
        
        Args:
            test_type: Tipo do teste (wechsler, personality, projective)
            **kwargs: Argumentos adicionais para o construtor do processador
            
        Returns:
            Instância do processador apropriado
            
        Raises:
            ValueError: Se o tipo de teste não for suportado
        """
        if test_type.lower() not in cls._processors:
            raise ValueError(
                f"Tipo de teste não suportado: {test_type}. "
                f"Tipos suportados: {', '.join(cls._processors.keys())}"
            )
        
        processor_class = cls._processors[test_type.lower()]
        return processor_class(**kwargs)
    
    @classmethod
    def register_processor(cls, test_type: str, processor_class: Type[BaseTestProcessor]):
        """
        Registra um novo tipo de processador.
        
        Args:
            test_type: Tipo do teste
            processor_class: Classe do processador
        """
        if not issubclass(processor_class, BaseTestProcessor):
            raise ValueError(
                f"A classe {processor_class.__name__} deve herdar de BaseTestProcessor"
            )
        
        cls._processors[test_type.lower()] = processor_class
    
    @classmethod
    def get_supported_types(cls) -> List[str]:
        """
        Retorna a lista de tipos de testes suportados.
        
        Returns:
            Lista de tipos de testes
        """
        return list(cls._processors.keys())
    
    @classmethod
    def is_supported(cls, test_type: str) -> bool:
        """
        Verifica se um tipo de teste é suportado.
        
        Args:
            test_type: Tipo do teste
            
        Returns:
            bool indicando se o tipo é suportado
        """
        return test_type.lower() in cls._processors 
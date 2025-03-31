"""
Testes para a factory de processadores de testes psicológicos.
"""
import pytest
from app.core.test_processors import (
    TestProcessorFactory,
    BaseTestProcessor,
    WechslerProcessor,
    PersonalityProcessor,
    ProjectiveProcessor
)

def test_processor_factory_create_processor():
    """Testa a criação de processadores pela factory."""
    # Teste para Wechsler
    processor = TestProcessorFactory.create_processor("wechsler")
    assert isinstance(processor, WechslerProcessor)
    
    # Teste para Personalidade
    processor = TestProcessorFactory.create_processor("personality")
    assert isinstance(processor, PersonalityProcessor)
    
    # Teste para Projetivo
    processor = TestProcessorFactory.create_processor("projective")
    assert isinstance(processor, ProjectiveProcessor)
    
    # Teste com argumentos adicionais
    processor = TestProcessorFactory.create_processor("wechsler", version="WISC-IV")
    assert processor.version == "WISC-IV"

def test_processor_factory_invalid_type():
    """Testa a criação de processador com tipo inválido."""
    with pytest.raises(ValueError) as exc_info:
        TestProcessorFactory.create_processor("tipo_invalido")
    assert "Tipo de teste não suportado" in str(exc_info.value)

def test_processor_factory_register_processor():
    """Testa o registro de um novo processador."""
    class NovoProcessor(BaseTestProcessor):
        def processar_dados(self, dados):
            return {}
        
        def calcular_escores(self, dados_processados):
            return {}
        
        def interpretar_resultados(self, escores):
            return {}
        
        def gerar_relatorio(self, interpretacao):
            return ""
    
    TestProcessorFactory.register_processor("novo", NovoProcessor)
    processor = TestProcessorFactory.create_processor("novo")
    assert isinstance(processor, NovoProcessor)

def test_processor_factory_register_invalid_processor():
    """Testa o registro de um processador inválido."""
    class ProcessadorInvalido:
        pass
    
    with pytest.raises(ValueError) as exc_info:
        TestProcessorFactory.register_processor("invalido", ProcessadorInvalido)
    assert "deve herdar de BaseTestProcessor" in str(exc_info.value)

def test_processor_factory_get_supported_types():
    """Testa a obtenção dos tipos de processadores suportados."""
    tipos = TestProcessorFactory.get_supported_types()
    assert isinstance(tipos, list)
    assert "wechsler" in tipos
    assert "personality" in tipos
    assert "projective" in tipos

def test_processor_factory_is_supported():
    """Testa a verificação de tipos suportados."""
    assert TestProcessorFactory.is_supported("wechsler") is True
    assert TestProcessorFactory.is_supported("personality") is True
    assert TestProcessorFactory.is_supported("projective") is True
    assert TestProcessorFactory.is_supported("tipo_invalido") is False 
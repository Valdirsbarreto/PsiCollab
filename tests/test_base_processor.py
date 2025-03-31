"""
Testes para o processador base de testes psicológicos.
"""
import pytest
from datetime import datetime
from app.core.test_processors import BaseTestProcessor

class TestBaseProcessor(BaseTestProcessor):
    """Classe de teste que implementa os métodos abstratos."""
    
    def processar_dados(self, dados):
        return {"processado": True}
    
    def calcular_escores(self, dados_processados):
        return {"escores": [1, 2, 3]}
    
    def interpretar_resultados(self, escores):
        return {"interpretacao": "Teste"}
    
    def gerar_relatorio(self, interpretacao):
        return "Relatório de teste"

def test_base_processor_initialization():
    """Testa a inicialização do processador base."""
    processor = TestBaseProcessor()
    assert processor.test_type == ""
    assert processor.version == ""
    assert processor.normas == {}
    assert processor.resultados == {}
    assert processor.interpretacao == {}
    assert processor.data_processamento is None

def test_base_processor_validar_dados():
    """Testa a validação de dados do processador base."""
    processor = TestBaseProcessor()
    assert processor.validar_dados({}) is True
    assert processor.validar_dados(None) is False

def test_base_processor_aplicar_normas():
    """Testa a aplicação de normas do processador base."""
    processor = TestBaseProcessor()
    escores = {"teste": 10}
    assert processor.aplicar_normas(escores) == escores

def test_base_processor_processar_teste():
    """Testa o processamento completo do teste."""
    processor = TestBaseProcessor()
    dados = {"teste": "dados"}
    
    resultado = processor.processar_teste(dados)
    
    assert isinstance(resultado, dict)
    assert "test_type" in resultado
    assert "version" in resultado
    assert "data_processamento" in resultado
    assert "resultados" in resultado
    assert "interpretacao" in resultado
    assert "relatorio" in resultado
    assert isinstance(resultado["data_processamento"], str)
    assert isinstance(processor.data_processamento, datetime) 
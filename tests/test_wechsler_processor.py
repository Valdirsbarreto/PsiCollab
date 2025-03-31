"""
Testes para o processador de testes de Wechsler.
"""
import pytest
from app.core.test_processors import WechslerProcessor

@pytest.fixture
def dados_wechsler():
    """Dados de exemplo para o teste de Wechsler."""
    return {
        "Compreensão Verbal": {
            "escore_bruto": 12,
            "tempo": 120,
            "observacoes": "Bom desempenho"
        },
        "Raciocínio Perceptivo": {
            "escore_bruto": 15,
            "tempo": 90,
            "observacoes": "Excelente"
        },
        "Memória de Trabalho": {
            "escore_bruto": 10,
            "tempo": 150,
            "observacoes": "Normal"
        },
        "Velocidade de Processamento": {
            "escore_bruto": 8,
            "tempo": 180,
            "observacoes": "Atenção necessária"
        }
    }

def test_wechsler_processor_initialization():
    """Testa a inicialização do processador Wechsler."""
    processor = WechslerProcessor()
    assert processor.test_type == "Wechsler"
    assert processor.version == "WAIS-IV"
    assert "escore_bruto" in processor.normas
    assert "escore_total" in processor.normas

def test_wechsler_processor_processar_dados(dados_wechsler):
    """Testa o processamento de dados do teste Wechsler."""
    processor = WechslerProcessor()
    dados_processados = processor.processar_dados(dados_wechsler)
    
    assert "subtestes" in dados_processados
    assert "escores_compostos" in dados_processados
    assert "escore_total" in dados_processados
    assert len(dados_processados["subtestes"]) == 4

def test_wechsler_processor_calcular_escores(dados_wechsler):
    """Testa o cálculo de escores do teste Wechsler."""
    processor = WechslerProcessor()
    dados_processados = processor.processar_dados(dados_wechsler)
    escores = processor.calcular_escores(dados_processados)
    
    assert "subtestes" in escores
    assert "escores_compostos" in escores
    assert "escore_total" in escores
    assert all(isinstance(escore, dict) for escore in escores["subtestes"].values())

def test_wechsler_processor_interpretar_resultados(dados_wechsler):
    """Testa a interpretação dos resultados do teste Wechsler."""
    processor = WechslerProcessor()
    dados_processados = processor.processar_dados(dados_wechsler)
    escores = processor.calcular_escores(dados_processados)
    interpretacao = processor.interpretar_resultados(escores)
    
    assert "nivel_intelectual" in interpretacao
    assert "perfil_cognitivo" in interpretacao
    assert "pontos_fortes" in interpretacao
    assert "pontos_fracos" in interpretacao
    assert "recomendacoes" in interpretacao

def test_wechsler_processor_gerar_relatorio(dados_wechsler):
    """Testa a geração de relatório do teste Wechsler."""
    processor = WechslerProcessor()
    dados_processados = processor.processar_dados(dados_wechsler)
    escores = processor.calcular_escores(dados_processados)
    interpretacao = processor.interpretar_resultados(escores)
    relatorio = processor.gerar_relatorio(interpretacao)
    
    assert isinstance(relatorio, str)
    assert "RELATÓRIO DE AVALIAÇÃO" in relatorio
    assert "Nível Intelectual" in relatorio
    assert "Perfil Cognitivo" in relatorio
    assert "Pontos Fortes" in relatorio
    assert "Pontos de Atenção" in relatorio
    assert "Recomendações" in relatorio

def test_wechsler_processor_validar_dados():
    """Testa a validação de dados do teste Wechsler."""
    processor = WechslerProcessor()
    
    # Dados válidos
    dados_validos = {
        "Compreensão Verbal": {"escore_bruto": 10},
        "Raciocínio Perceptivo": {"escore_bruto": 10},
        "Memória de Trabalho": {"escore_bruto": 10},
        "Velocidade de Processamento": {"escore_bruto": 10}
    }
    assert processor._validar_dados_wechsler(dados_validos) is True
    
    # Dados inválidos
    dados_invalidos = {
        "Compreensão Verbal": {"escore_bruto": 10},
        "Raciocínio Perceptivo": {"escore_bruto": 10}
    }
    assert processor._validar_dados_wechsler(dados_invalidos) is False 
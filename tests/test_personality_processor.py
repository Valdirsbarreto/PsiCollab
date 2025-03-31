"""
Testes para o processador de testes de personalidade.
"""
import pytest
from app.core.test_processors import PersonalityProcessor

@pytest.fixture
def dados_mmpi():
    """Dados de exemplo para o teste MMPI-2."""
    return {
        "Hipocondria": {
            "escore_bruto": 65,
            "respostas": [1, 1, 0, 1, 1],
            "tempo": 120
        },
        "Depressão": {
            "escore_bruto": 70,
            "respostas": [1, 1, 1, 0, 1],
            "tempo": 150
        },
        "Histeria": {
            "escore_bruto": 55,
            "respostas": [0, 1, 1, 1, 0],
            "tempo": 100
        },
        "Desvio Psicopático": {
            "escore_bruto": 60,
            "respostas": [1, 0, 1, 1, 1],
            "tempo": 130
        },
        "Masculinidade/Feminilidade": {
            "escore_bruto": 45,
            "respostas": [0, 1, 0, 1, 0],
            "tempo": 110
        },
        "Paranóia": {
            "escore_bruto": 75,
            "respostas": [1, 1, 1, 1, 1],
            "tempo": 140
        },
        "Psicastenia": {
            "escore_bruto": 80,
            "respostas": [1, 1, 1, 1, 1],
            "tempo": 160
        },
        "Esquizofrenia": {
            "escore_bruto": 85,
            "respostas": [1, 1, 1, 1, 1],
            "tempo": 170
        },
        "Hipomania": {
            "escore_bruto": 50,
            "respostas": [0, 0, 1, 0, 1],
            "tempo": 90
        },
        "Introversão Social": {
            "escore_bruto": 40,
            "respostas": [0, 0, 0, 1, 0],
            "tempo": 100
        },
        "validacao": {
            "L": 45,
            "F": 55,
            "K": 50
        },
        "observacoes": {
            "comportamento": "Cooperativo",
            "humor": "Ansioso",
            "observacoes_gerais": "Boa adesão ao teste"
        }
    }

def test_personality_processor_initialization():
    """Testa a inicialização do processador de personalidade."""
    processor = PersonalityProcessor()
    assert processor.test_type == "MMPI-2"
    assert processor.version == "2.0"
    assert "MMPI-2" in processor.config
    assert "NEO-PI-R" in processor.config

def test_personality_processor_processar_dados(dados_mmpi):
    """Testa o processamento de dados do teste de personalidade."""
    processor = PersonalityProcessor()
    dados_processados = processor.processar_dados(dados_mmpi)
    
    assert "escalas" in dados_processados
    assert "escores_validacao" in dados_processados
    assert "observacoes" in dados_processados
    assert len(dados_processados["escalas"]) == 10

def test_personality_processor_calcular_escores(dados_mmpi):
    """Testa o cálculo de escores do teste de personalidade."""
    processor = PersonalityProcessor()
    dados_processados = processor.processar_dados(dados_mmpi)
    escores = processor.calcular_escores(dados_processados)
    
    assert "escalas" in escores
    assert "escores_validacao" in escores
    assert "perfil" in escores
    assert all(isinstance(escore, dict) for escore in escores["escalas"].values())

def test_personality_processor_interpretar_resultados(dados_mmpi):
    """Testa a interpretação dos resultados do teste de personalidade."""
    processor = PersonalityProcessor()
    dados_processados = processor.processar_dados(dados_mmpi)
    escores = processor.calcular_escores(dados_processados)
    interpretacao = processor.interpretar_resultados(escores)
    
    assert "validade" in interpretacao
    assert "perfil_personalidade" in interpretacao
    assert "caracteristicas_principais" in interpretacao
    assert "pontos_atencao" in interpretacao
    assert "recomendacoes" in interpretacao

def test_personality_processor_gerar_relatorio(dados_mmpi):
    """Testa a geração de relatório do teste de personalidade."""
    processor = PersonalityProcessor()
    dados_processados = processor.processar_dados(dados_mmpi)
    escores = processor.calcular_escores(dados_processados)
    interpretacao = processor.interpretar_resultados(escores)
    relatorio = processor.gerar_relatorio(interpretacao)
    
    assert isinstance(relatorio, str)
    assert "RELATÓRIO DE AVALIAÇÃO" in relatorio
    assert "Validade do Teste" in relatorio
    assert "Perfil de Personalidade" in relatorio
    assert "Características Principais" in relatorio
    assert "Pontos de Atenção" in relatorio
    assert "Recomendações" in relatorio

def test_personality_processor_validar_dados():
    """Testa a validação de dados do teste de personalidade."""
    processor = PersonalityProcessor()
    
    # Dados válidos
    dados_validos = {
        "Hipocondria": {"escore_bruto": 50},
        "Depressão": {"escore_bruto": 50},
        "Histeria": {"escore_bruto": 50},
        "Desvio Psicopático": {"escore_bruto": 50},
        "Masculinidade/Feminilidade": {"escore_bruto": 50},
        "Paranóia": {"escore_bruto": 50},
        "Psicastenia": {"escore_bruto": 50},
        "Esquizofrenia": {"escore_bruto": 50},
        "Hipomania": {"escore_bruto": 50},
        "Introversão Social": {"escore_bruto": 50}
    }
    assert processor._validar_dados_personalidade(dados_validos) is True
    
    # Dados inválidos
    dados_invalidos = {
        "Hipocondria": {"escore_bruto": 50},
        "Depressão": {"escore_bruto": 50}
    }
    assert processor._validar_dados_personalidade(dados_invalidos) is False 
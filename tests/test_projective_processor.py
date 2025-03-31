"""
Testes para o processador de testes projetivos.
"""
import pytest
from app.core.test_processors import ProjectiveProcessor

@pytest.fixture
def dados_rorschach():
    """Dados de exemplo para o teste de Rorschach."""
    return {
        "1": {
            "conteudo": "Borboleta",
            "localizacao": "W",
            "determinantes": ["F", "C"],
            "tempo": 15
        },
        "2": {
            "conteudo": "Dois ursos",
            "localizacao": "D",
            "determinantes": ["F", "M"],
            "tempo": 20
        },
        "3": {
            "conteudo": "Pessoas dançando",
            "localizacao": "D",
            "determinantes": ["M", "C"],
            "tempo": 25
        },
        "4": {
            "conteudo": "Monstro",
            "localizacao": "W",
            "determinantes": ["F", "C", "Y"],
            "tempo": 30
        },
        "5": {
            "conteudo": "Morcego",
            "localizacao": "W",
            "determinantes": ["F"],
            "tempo": 18
        },
        "6": {
            "conteudo": "Pele de animal",
            "localizacao": "D",
            "determinantes": ["T"],
            "tempo": 22
        },
        "7": {
            "conteudo": "Duas mulheres",
            "localizacao": "D",
            "determinantes": ["F", "M"],
            "tempo": 28
        },
        "8": {
            "conteudo": "Animais",
            "localizacao": "D",
            "determinantes": ["F", "C"],
            "tempo": 24
        },
        "9": {
            "conteudo": "Fogo",
            "localizacao": "D",
            "determinantes": ["C", "Y"],
            "tempo": 19
        },
        "10": {
            "conteudo": "Caranguejo",
            "localizacao": "W",
            "determinantes": ["F"],
            "tempo": 16
        },
        "comportamento": {
            "atitude": "Cooperativa",
            "humor": "Ansioso",
            "observacoes": "Boa adesão ao teste"
        },
        "observacoes": {
            "tempo_total": 217,
            "respostas_por_laminas": [1, 2, 1, 1, 1, 1, 2, 1, 1, 1],
            "observacoes_gerais": "Bom desempenho"
        }
    }

def test_projective_processor_initialization():
    """Testa a inicialização do processador projetivo."""
    processor = ProjectiveProcessor()
    assert processor.test_type == "Rorschach"
    assert processor.version == "1.0"
    assert "Rorschach" in processor.config
    assert "TAT" in processor.config

def test_projective_processor_processar_dados(dados_rorschach):
    """Testa o processamento de dados do teste projetivo."""
    processor = ProjectiveProcessor()
    dados_processados = processor.processar_dados(dados_rorschach)
    
    assert "respostas" in dados_processados
    assert "tempos" in dados_processados
    assert "observacoes" in dados_processados
    assert "comportamento" in dados_processados
    assert len(dados_processados["respostas"]) == 10

def test_projective_processor_calcular_escores(dados_rorschach):
    """Testa o cálculo de escores do teste projetivo."""
    processor = ProjectiveProcessor()
    dados_processados = processor.processar_dados(dados_rorschach)
    escores = processor.calcular_escores(dados_processados)
    
    assert "respostas" in escores
    assert "indices" in escores
    assert "perfil" in escores
    assert all(isinstance(escore, dict) for escore in escores["respostas"].values())

def test_projective_processor_interpretar_resultados(dados_rorschach):
    """Testa a interpretação dos resultados do teste projetivo."""
    processor = ProjectiveProcessor()
    dados_processados = processor.processar_dados(dados_rorschach)
    escores = processor.calcular_escores(dados_processados)
    interpretacao = processor.interpretar_resultados(escores)
    
    assert "validade" in interpretacao
    assert "perfil_personalidade" in interpretacao
    assert "caracteristicas_principais" in interpretacao
    assert "pontos_atencao" in interpretacao
    assert "recomendacoes" in interpretacao

def test_projective_processor_gerar_relatorio(dados_rorschach):
    """Testa a geração de relatório do teste projetivo."""
    processor = ProjectiveProcessor()
    dados_processados = processor.processar_dados(dados_rorschach)
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

def test_projective_processor_validar_dados():
    """Testa a validação de dados do teste projetivo."""
    processor = ProjectiveProcessor()
    
    # Dados válidos (70% das lâminas respondidas)
    dados_validos = {
        "1": {"conteudo": "Teste"},
        "2": {"conteudo": "Teste"},
        "3": {"conteudo": "Teste"},
        "4": {"conteudo": "Teste"},
        "5": {"conteudo": "Teste"},
        "6": {"conteudo": "Teste"},
        "7": {"conteudo": "Teste"}
    }
    assert processor._validar_dados_projetivo(dados_validos) is True
    
    # Dados inválidos (menos de 70% das lâminas respondidas)
    dados_invalidos = {
        "1": {"conteudo": "Teste"},
        "2": {"conteudo": "Teste"},
        "3": {"conteudo": "Teste"}
    }
    assert processor._validar_dados_projetivo(dados_invalidos) is False 
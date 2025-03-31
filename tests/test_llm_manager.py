"""
Testes para o gerenciador de LLM.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.core.llm_manager import LLMManager

@pytest.fixture
def llm_manager():
    """Fixture que cria uma instância do gerenciador de LLM."""
    return LLMManager()

@pytest.fixture
def resultados_wechsler():
    """Dados de exemplo para teste Wechsler."""
    return {
        "test_type": "WAIS-IV",
        "nivel_intelectual": "Superior",
        "perfil_cognitivo": "Verbal > Perceptivo",
        "pontos_fortes": ["Compreensão Verbal", "Memória de Trabalho"],
        "pontos_fracos": ["Velocidade de Processamento"]
    }

@pytest.fixture
def resultados_personalidade():
    """Dados de exemplo para teste de personalidade."""
    return {
        "test_type": "MMPI-2",
        "validade": "Válido",
        "perfil_personalidade": "Ansioso-Depressivo",
        "caracteristicas_principais": ["Ansiedade", "Perfeccionismo"],
        "pontos_atencao": ["Tendência à ruminação"]
    }

@pytest.fixture
def resultados_projetivo():
    """Dados de exemplo para teste projetivo."""
    return {
        "test_type": "Rorschach",
        "validade": "Válido",
        "perfil_personalidade": "Introvertido-Reflexivo",
        "caracteristicas_principais": ["Criatividade", "Autocontrole"],
        "pontos_atencao": ["Rigidez cognitiva"]
    }

@pytest.mark.asyncio
async def test_llm_manager_initialization(llm_manager):
    """Testa a inicialização do gerenciador de LLM."""
    assert llm_manager.api_key is not None
    assert llm_manager.model is not None
    assert llm_manager.temperature is not None
    assert llm_manager.max_tokens is not None
    assert "wechsler" in llm_manager.templates
    assert "personality" in llm_manager.templates
    assert "projective" in llm_manager.templates

@pytest.mark.asyncio
async def test_gerar_interpretacao_avancada_wechsler(llm_manager, resultados_wechsler):
    """Testa a geração de interpretação avançada para teste Wechsler."""
    with patch("openai.ChatCompletion.acreate") as mock_create:
        # Configura o mock
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Interpretação detalhada"))
        ]
        mock_create.return_value = mock_response
        
        # Executa o teste
        resultado = await llm_manager.gerar_interpretacao_avancada(
            "wechsler", resultados_wechsler
        )
        
        # Verifica o resultado
        assert isinstance(resultado, dict)
        assert "test_type" in resultado
        assert "data_interpretacao" in resultado
        assert "interpretacao_avancada" in resultado
        assert "modelo_utilizado" in resultado
        assert "parametros" in resultado
        
        # Verifica a chamada à API
        mock_create.assert_called_once()
        call_args = mock_create.call_args[1]
        assert call_args["model"] == llm_manager.model
        assert "messages" in call_args
        assert len(call_args["messages"]) == 2

@pytest.mark.asyncio
async def test_gerar_interpretacao_avancada_invalid_type(llm_manager):
    """Testa a geração de interpretação com tipo inválido."""
    with pytest.raises(ValueError) as exc_info:
        await llm_manager.gerar_interpretacao_avancada(
            "tipo_invalido", {}
        )
    assert "Tipo de teste não suportado" in str(exc_info.value)

@pytest.mark.asyncio
async def test_gerar_recomendacoes_personalizadas(llm_manager, resultados_wechsler):
    """Testa a geração de recomendações personalizadas."""
    with patch("openai.ChatCompletion.acreate") as mock_create:
        # Configura o mock
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="1. Recomendação 1\n2. Recomendação 2"))
        ]
        mock_create.return_value = mock_response
        
        # Executa o teste
        recomendacoes = await llm_manager.gerar_recomendacoes_personalizadas(
            "wechsler", resultados_wechsler
        )
        
        # Verifica o resultado
        assert isinstance(recomendacoes, list)
        assert len(recomendacoes) <= 5
        assert all(isinstance(r, str) for r in recomendacoes)
        
        # Verifica a chamada à API
        mock_create.assert_called_once()
        call_args = mock_create.call_args[1]
        assert call_args["model"] == llm_manager.model
        assert "messages" in call_args
        assert len(call_args["messages"]) == 2

@pytest.mark.asyncio
async def test_gerar_relatorio_completo(llm_manager, resultados_wechsler):
    """Testa a geração de relatório completo."""
    with patch("openai.ChatCompletion.acreate") as mock_create:
        # Configura o mock
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Conteúdo do relatório"))
        ]
        mock_create.return_value = mock_response
        
        # Executa o teste
        relatorio = await llm_manager.gerar_relatorio_completo(
            "wechsler", resultados_wechsler
        )
        
        # Verifica o resultado
        assert isinstance(relatorio, dict)
        assert "test_type" in relatorio
        assert "data_geracao" in relatorio
        assert "resultados_brutos" in relatorio
        assert "interpretacao_avancada" in relatorio
        assert "recomendacoes_personalizadas" in relatorio
        assert "modelo_utilizado" in relatorio
        
        # Verifica as chamadas à API
        assert mock_create.call_count == 2

@pytest.mark.asyncio
async def test_gerar_relatorio_completo_com_contexto(llm_manager, resultados_wechsler):
    """Testa a geração de relatório completo com contexto adicional."""
    contexto = {
        "idade": 25,
        "escolaridade": "Superior Completo",
        "motivo_avaliacao": "Orientação Profissional"
    }
    
    with patch("openai.ChatCompletion.acreate") as mock_create:
        # Configura o mock
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Conteúdo do relatório"))
        ]
        mock_create.return_value = mock_response
        
        # Executa o teste
        relatorio = await llm_manager.gerar_relatorio_completo(
            "wechsler", resultados_wechsler, contexto
        )
        
        # Verifica o resultado
        assert "contexto" in relatorio
        assert relatorio["contexto"] == contexto 
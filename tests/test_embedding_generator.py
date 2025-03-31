"""
Testes para o gerador de embeddings da base de conhecimento.
"""
import pytest
import json
import os
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
from app.core.embedding_generator import EmbeddingGenerator

@pytest.fixture
def embedding_generator():
    """Cria uma instância do EmbeddingGenerator para testes."""
    return EmbeddingGenerator()

@pytest.fixture
def documento_exemplo():
    """Cria um documento de exemplo para testes."""
    return {
        "id": "doc_001",
        "conteudo": "Este é um texto de exemplo para teste de embeddings.",
        "tipo": "teste",
        "metadata": {
            "categoria": "testes",
            "autor": "teste",
            "data_criacao": datetime.now().isoformat()
        }
    }

@pytest.fixture
def embedding_exemplo():
    """Cria um embedding de exemplo para testes."""
    return [0.1, 0.2, 0.3, 0.4, 0.5]

@pytest.mark.asyncio
async def test_gerar_embedding(embedding_generator, embedding_exemplo):
    """Testa a geração de embeddings."""
    # Mock da resposta da API
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"embedding": embedding_exemplo})
    
    # Mock da sessão HTTP
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        resultado = await embedding_generator.gerar_embedding("texto teste")
        assert resultado == embedding_exemplo

@pytest.mark.asyncio
async def test_gerar_embedding_erro(embedding_generator):
    """Testa o tratamento de erro na geração de embeddings."""
    # Mock da resposta da API com erro
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.text = AsyncMock(return_value="Erro interno")
    
    # Mock da sessão HTTP
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        resultado = await embedding_generator.gerar_embedding("texto teste")
        assert resultado == []

def test_validar_documento(embedding_generator, documento_exemplo):
    """Testa a validação de documentos."""
    # Teste com documento válido
    assert embedding_generator._validar_documento(documento_exemplo) is True
    
    # Teste com documento inválido
    documento_invalido = {"id": "doc_001"}  # Faltando campos obrigatórios
    assert embedding_generator._validar_documento(documento_invalido) is False

@pytest.mark.asyncio
async def test_processar_documento(embedding_generator, documento_exemplo, embedding_exemplo):
    """Testa o processamento de um documento."""
    # Mock da geração de embedding
    with patch.object(embedding_generator, "gerar_embedding", return_value=embedding_exemplo):
        resultado = await embedding_generator.processar_documento(documento_exemplo)
        
        assert resultado["id"] == documento_exemplo["id"]
        assert resultado["embedding"] == embedding_exemplo
        assert "data_processamento" in resultado

@pytest.mark.asyncio
async def test_processar_documento_invalido(embedding_generator):
    """Testa o processamento de um documento inválido."""
    documento_invalido = {"id": "doc_001"}  # Faltando campos obrigatórios
    
    with pytest.raises(ValueError):
        await embedding_generator.processar_documento(documento_invalido)

@pytest.mark.asyncio
async def test_processar_lote(embedding_generator, documento_exemplo, embedding_exemplo):
    """Testa o processamento de um lote de documentos."""
    documentos = [documento_exemplo] * 3
    
    # Mock da geração de embedding
    with patch.object(embedding_generator, "processar_documento", return_value={
        **documento_exemplo,
        "embedding": embedding_exemplo,
        "data_processamento": datetime.now().isoformat()
    }):
        resultado = await embedding_generator.processar_lote(documentos)
        
        assert len(resultado) == 3
        assert all("embedding" in doc for doc in resultado)
        assert all("data_processamento" in doc for doc in resultado)

@pytest.mark.asyncio
async def test_armazenar_na_vector_db(embedding_generator, documento_exemplo, embedding_exemplo):
    """Testa o armazenamento de documentos na Vector DB."""
    documentos = [{
        **documento_exemplo,
        "embedding": embedding_exemplo,
        "data_processamento": datetime.now().isoformat()
    }]
    
    # Mock da resposta da Vector DB
    mock_response = AsyncMock()
    mock_response.status = 200
    
    # Mock da sessão HTTP
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        resultado = await embedding_generator.armazenar_na_vector_db(documentos)
        assert resultado is True

@pytest.mark.asyncio
async def test_armazenar_na_vector_db_erro(embedding_generator, documento_exemplo, embedding_exemplo):
    """Testa o tratamento de erro no armazenamento na Vector DB."""
    documentos = [{
        **documento_exemplo,
        "embedding": embedding_exemplo,
        "data_processamento": datetime.now().isoformat()
    }]
    
    # Mock da resposta da Vector DB com erro
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.text = AsyncMock(return_value="Erro interno")
    
    # Mock da sessão HTTP
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
    
    with patch("aiohttp.ClientSession", return_value=mock_session):
        resultado = await embedding_generator.armazenar_na_vector_db(documentos)
        assert resultado is False

@pytest.mark.asyncio
async def test_processar_arquivo_json(embedding_generator, documento_exemplo, embedding_exemplo, tmp_path):
    """Testa o processamento de um arquivo JSON."""
    # Cria um arquivo JSON temporário
    documentos = [documento_exemplo] * 3
    arquivo_json = tmp_path / "documentos.json"
    
    with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump(documentos, f)
    
    # Mock do processamento de lote
    documento_processado = {
        **documento_exemplo,
        "embedding": embedding_exemplo,
        "data_processamento": datetime.now().isoformat()
    }
    
    with patch.object(embedding_generator, "processar_lote", return_value=[documento_processado] * 3), \
         patch.object(embedding_generator, "armazenar_na_vector_db", return_value=True):
        
        total, processados = await embedding_generator.processar_arquivo_json(str(arquivo_json))
        assert total == 3
        assert processados == 3

@pytest.mark.asyncio
async def test_processar_arquivo_json_erro(embedding_generator, tmp_path):
    """Testa o tratamento de erro no processamento de arquivo JSON."""
    # Cria um arquivo JSON inválido
    arquivo_json = tmp_path / "documentos_invalidos.json"
    with open(arquivo_json, "w", encoding="utf-8") as f:
        f.write("arquivo inválido")
    
    total, processados = await embedding_generator.processar_arquivo_json(str(arquivo_json))
    assert total == 0
    assert processados == 0 
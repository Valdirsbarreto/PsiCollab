import pytest
import httpx
import json

@pytest.mark.integration
async def test_qdrant_health():
    """Teste de integração do serviço Qdrant"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:6333/healthz", timeout=2.0)
            if response.status_code == 404:
                pytest.skip("Endpoint de health check não encontrado - teste pulado")
            assert response.status_code == 200
            assert response.content == b'healthz check passed'
    except (httpx.RequestError, httpx.TimeoutException):
        pytest.skip("Serviço Qdrant não está disponível - teste pulado")

@pytest.mark.integration
async def test_qdrant_collections():
    """Teste de listagem de coleções do Qdrant"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:6333/collections", timeout=2.0)
            assert response.status_code == 200
            data = response.json()
            assert "result" in data
            assert "collections" in data["result"]
            assert isinstance(data["result"]["collections"], list)
    except (httpx.RequestError, httpx.TimeoutException):
        pytest.skip("Serviço Qdrant não está disponível - teste pulado")

@pytest.mark.integration
async def test_qdrant_create_collection():
    """Teste de criação de coleção no Qdrant"""
    try:
        async with httpx.AsyncClient() as client:
            # Criar uma coleção de teste
            collection_name = "test_collection"
            payload = {
                "vectors": {
                    "size": 384,
                    "distance": "Cosine"
                }
            }
            
            # Primeiro tenta deletar a coleção se ela existir
            await client.delete(f"http://localhost:6333/collections/{collection_name}")
            
            # Cria a coleção
            response = await client.put(
                f"http://localhost:6333/collections/{collection_name}",
                json=payload,
                timeout=2.0
            )
            assert response.status_code in [200, 201]
            
            # Verifica se a coleção foi criada
            response = await client.get(f"http://localhost:6333/collections/{collection_name}")
            assert response.status_code == 200
            
            # Limpa: remove a coleção de teste
            response = await client.delete(f"http://localhost:6333/collections/{collection_name}")
            assert response.status_code == 200
    except (httpx.RequestError, httpx.TimeoutException):
        pytest.skip("Serviço Qdrant não está disponível - teste pulado") 
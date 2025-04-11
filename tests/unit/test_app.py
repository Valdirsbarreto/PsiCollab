import pytest

# Removendo importações redundantes
# import sys
# import os
# from fastapi.testclient import TestClient
# 
# # Adiciona o diretório raiz ao path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# 
# from app.psicollab_app import app
# 
# client = TestClient(app)

@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.unit
async def test_read_health(client):  # client é agora AsyncClient
    """Teste básico do endpoint de health check"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.unit
async def test_read_root(client):  # client é agora AsyncClient
    """Teste básico do endpoint raiz"""
    response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.unit
async def test_protected_route_unauthorized(client):  # client é agora AsyncClient
    """Teste de rota protegida sem autenticação"""
    response = await client.get("/api/protected")
    assert response.status_code in [401, 403]  # Aceita tanto Unauthorized quanto Forbidden

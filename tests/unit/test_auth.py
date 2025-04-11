import pytest
import os
from unittest.mock import patch

# Removendo importações redundantes
# from fastapi.testclient import TestClient
# from app.psicollab_app import app
# client = TestClient(app)

@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.skip(reason="Aguardando implementação completa do frontend e fluxo de autenticação Google")
@pytest.mark.unit
async def test_google_auth_redirect(client):  # client é agora AsyncClient
    """Teste do endpoint de redirecionamento para autenticação Google"""
    # TODO: Implementar quando o frontend estiver pronto
    # - Adicionar mock do cliente OAuth2
    # - Verificar fluxo completo de autenticação
    # - Testar diferentes cenários de callback
    with patch.dict(os.environ, {
        'GOOGLE_CLIENT_ID': 'test_client_id',
        'GOOGLE_REDIRECT_URI': 'http://localhost:8080/api/auth/google/callback'
    }):
        response = await client.get("/api/auth/google")
        assert response.status_code in [200, 302]
        assert "accounts.google.com" in response.headers.get('location', '')

@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.unit
async def test_protected_route_with_invalid_token(client):  # client é agora AsyncClient
    """Teste de rota protegida com token inválido"""
    response = await client.get(
        "/api/protected",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code in [401, 403]
    
@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.unit
async def test_protected_route_without_token(client):  # client é agora AsyncClient
    """Teste de rota protegida sem token"""
    response = await client.get("/api/protected")
    assert response.status_code in [401, 403]

@pytest.mark.asyncio  # Marca o teste como assíncrono
@pytest.mark.unit
async def test_protected_route_with_invalid_header(client):  # client é agora AsyncClient
    """Teste de rota protegida com header inválido"""
    response = await client.get(
        "/api/protected",
        headers={"Authorization": "InvalidFormat token123"}
    )
    assert response.status_code in [401, 403]

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os
from psicollab_app import app

client = TestClient(app)

@pytest.mark.skip(reason="Aguardando implementação completa do frontend e fluxo de autenticação Google")
@pytest.mark.unit
def test_google_auth_redirect():
    """Teste do endpoint de redirecionamento para autenticação Google"""
    # TODO: Implementar quando o frontend estiver pronto
    # - Adicionar mock do cliente OAuth2
    # - Verificar fluxo completo de autenticação
    # - Testar diferentes cenários de callback
    with patch.dict(os.environ, {
        'GOOGLE_CLIENT_ID': 'test_client_id',
        'GOOGLE_REDIRECT_URI': 'http://localhost:8080/api/auth/google/callback'
    }):
        response = client.get("/api/auth/google")
        assert response.status_code in [200, 302]
        assert "accounts.google.com" in response.headers.get('location', '')

@pytest.mark.unit
def test_protected_route_with_invalid_token():
    """Teste de rota protegida com token inválido"""
    response = client.get(
        "/api/protected",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code in [401, 403]
    
@pytest.mark.unit
def test_protected_route_without_token():
    """Teste de rota protegida sem token"""
    response = client.get("/api/protected")
    assert response.status_code in [401, 403]

@pytest.mark.unit
def test_protected_route_with_invalid_header():
    """Teste de rota protegida com header inválido"""
    response = client.get(
        "/api/protected",
        headers={"Authorization": "InvalidFormat token123"}
    )
    assert response.status_code in [401, 403] 
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from psicollab_app import app

client = TestClient(app)

@pytest.mark.unit
def test_read_health():
    """Teste básico do endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

@pytest.mark.unit
def test_read_root():
    """Teste básico do endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.unit
def test_protected_route_unauthorized():
    """Teste de rota protegida sem autenticação"""
    response = client.get("/api/protected")
    assert response.status_code in [401, 403]  # Aceita tanto Unauthorized quanto Forbidden 
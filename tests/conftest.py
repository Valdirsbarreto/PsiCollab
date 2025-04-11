import os
import pytest
from httpx import AsyncClient

# Não precisamos mais manipular o sys.path - o pytest.ini cuida disso
from app.psicollab_app import app

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
async def client():
    # Mock das variáveis de ambiente
    os.environ["GOOGLE_CLIENT_ID"] = "fake-client-id"
    os.environ["GOOGLE_REDIRECT_URI"] = "http://localhost:8080/api/auth/google/callback"
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

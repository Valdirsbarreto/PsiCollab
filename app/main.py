"""
Aplicativo principal do PsiCollab.
"""
import logging
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import api_router
from app.core.config import settings

# Configuração de logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Criação do aplicativo
app = FastAPI(
    title="PsiCollab API",
    description="API para o sistema PsiCollab de assistência a laudos psicológicos",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, limitar aos domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir as rotas da API
app.include_router(api_router, prefix="/api")

# Rota raiz
@app.get("/")
async def root():
    """
    Retorna informações básicas sobre a API.
    """
    return {
        "name": "PsiCollab API",
        "version": "0.1.0",
        "status": "online"
    }

# Rota de status de saúde
@app.get("/health")
async def health():
    """
    Verifica o status de saúde da API e seus componentes.
    """
    return {
        "status": "ok",
        "message": "API está funcionando corretamente"
    }

if __name__ == "__main__":
    # Configuração do servidor
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="debug"
    ) 
"""
Aplicativo principal do PsiCollab
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import system_router, auth_router, protected_router

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do app
app = FastAPI(
    title="PsiCollab API",
    description="API para o sistema PsiCollab de assistência na elaboração de laudos psicológicos",
    version="0.1.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo routers
app.include_router(system_router)
app.include_router(auth_router)
app.include_router(protected_router) 
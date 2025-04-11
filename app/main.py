"""
Aplicativo principal do PsiCollab
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

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
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://0.0.0.0",
    "http://0.0.0.0:8080",
    # Adiciona suporte a HTTPS também
    "https://localhost",
    "https://localhost:8080",
    "https://127.0.0.1",
    "https://127.0.0.1:8080",
    # Permite requisições do mesmo host
    "null",
    "*"
]

# Configuração detalhada do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "X-Requested-With",
        "Accept",
        "Origin"
    ],
    expose_headers=["*"],
    max_age=86400  # 24 horas em segundos
)

# Configuração dos arquivos estáticos
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "static")
logger.info(f"Diretório de arquivos estáticos: {static_dir}")

# Configuração para servir arquivos estáticos com cabeçalhos CORS
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    if "/static/" in request.url.path:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Cache-Control"] = "no-cache"
    return response

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Incluindo routers
app.include_router(system_router)
app.include_router(auth_router)
app.include_router(protected_router) 
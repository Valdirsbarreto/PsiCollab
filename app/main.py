from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import logging
import os
from typing import Optional

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('psicollab.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuração do FastAPI
app = FastAPI(
    title="PsiCollab API",
    description="API para o sistema PsiCollab - Assistente de IA para Psicólogos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substituir por origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.2f}s"
    )
    return response

# Função de autenticação
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: Implementar validação real do token
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# Rota de teste
@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API do PsiCollab",
        "status": "online",
        "version": "1.0.0"
    }

# Rota protegida de exemplo
@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {
        "message": "Rota protegida acessada com sucesso",
        "user": current_user
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
"""
Rotas da API PsiCollab
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

# Router para o sistema
system_router = APIRouter(
    prefix="",
    tags=["Sistema"]
)

# Router para autenticação
auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticação"]
)

# Router para rotas protegidas
protected_router = APIRouter(
    prefix="/api",
    tags=["Protegido"]
)

# Rotas do sistema
@system_router.get("/health")
async def health_check():
    """
    Verificação de saúde da API
    """
    return {"status": "online"}

@system_router.get("/")
async def root():
    """
    Rota principal - Retorna a página de login
    """
    return {"message": "Bem-vindo ao PsiCollab API"}

# Rotas de autenticação
@auth_router.get("/google")
async def google_auth():
    """
    Inicia o fluxo de autenticação com Google
    """
    return {"message": "Rota de autenticação Google"}

@auth_router.get("/callback")
async def google_callback(code: str = "default_code"):
    """
    Callback do Google OAuth2
    """
    return {"message": "Rota de callback Google", "code": code}

@auth_router.get("/me")
async def get_me():
    """
    Obtém informações do usuário autenticado
    """
    return {"message": "Informações do usuário"}

@auth_router.get("/phone")
async def phone_auth():
    """
    Rota para autenticação com telefone (mock)
    """
    return JSONResponse({"message": "Autenticação com telefone será implementada"})

# Rotas protegidas
@protected_router.get("/protected")
async def protected_route():
    """
    Exemplo de rota protegida
    """
    return {"message": "Rota protegida"} 
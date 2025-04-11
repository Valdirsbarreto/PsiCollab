"""
Rotas da API PsiCollab
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
from app.core.sms_auth import send_verification_code, verify_code, create_phone_token, validate_phone_token
from app.core.auth import get_current_user

# Configuração do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Modelos Pydantic para validação
class PhoneRequest(BaseModel):
    phone_number: str

class VerifyRequest(BaseModel):
    phone_number: str
    code: str

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

# Rotas de autenticação por telefone
@auth_router.post("/phone/request")
async def request_verification(phone_request: PhoneRequest):
    """
    Envia código de verificação via SMS
    """
    try:
        await send_verification_code(phone_request.phone_number)
        return {"message": "Código enviado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar código de verificação: {str(e)}")

@auth_router.post("/phone/verify")
async def verify_phone(verify_request: VerifyRequest):
    """
    Verifica o código recebido e retorna um token JWT
    """
    try:
        is_valid = await verify_code(verify_request.phone_number, verify_request.code)
        if is_valid:
            token = create_phone_token(verify_request.phone_number)
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail="Código inválido")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar código: {str(e)}")

# Rotas protegidas
@protected_router.get("/protected")
async def protected_route(request: Request, user_data: dict = Depends(get_current_user)):
    """
    Exemplo de rota protegida
    """
    logger.debug(f"Headers da requisição: {dict(request.headers)}")
    logger.debug(f"Dados do usuário: {user_data}")
    
    return {
        "message": "Rota protegida acessada com sucesso",
        "user": user_data
    } 
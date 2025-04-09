from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from pathlib import Path
import uvicorn
import logging
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import httpx
import json
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Google OAuth2
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8080/api/auth/google/callback"

# URLs do Google OAuth2
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Configurações JWT
SECRET_KEY = "PsiCollabSecretKey2024"  # Chave fixa para desenvolvimento
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuração do OAuth2
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obtém o usuário atual usando o token do Google"""
    try:
        # Remove qualquer prefixo 'Bearer' se existir
        token = credentials.credentials
        if token.startswith('"') and token.endswith('"'):
            token = token[1:-1]  # Remove aspas
        if token.startswith('Bearer '):
            token = token[7:]  # Remove 'Bearer '
            
        # Usa o token para obter informações do usuário diretamente do Google
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                logger.error(f"Erro na resposta do Google: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido ou expirado"
                )
            
            user_info = response.json()
            logger.debug(f"Informações do usuário obtidas com sucesso: {user_info.get('email')}")
            return user_info
            
    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro na validação do token: {str(e)}"
        )

# Inicialização do aplicativo
app = FastAPI(
    title="PsiCollab API",
    description="API para o sistema PsiCollab de assistência na elaboração de laudos psicológicos",
    version="0.1.0"
)

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens para teste
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas do sistema
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "online"}

@app.get("/", tags=["Sistema"])
async def root():
    """Página inicial"""
    return FileResponse('static/index.html')

# Rotas de autenticação
@app.get("/api/auth/google")
async def google_auth():
    """
    Endpoint para iniciar o fluxo de autenticação Google.
    Redireciona o usuário para a página de login do Google.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    if not client_id or not redirect_uri:
        raise HTTPException(
            status_code=500,
            detail="Configuração do Google OAuth não encontrada"
        )
    
    # Escopo para acessar informações básicas do perfil
    scope = "openid email profile"
    
    # URL de autorização do Google
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        "&response_type=code"
        "&access_type=offline"
    )
    
    return RedirectResponse(url=auth_url)

@app.get("/api/auth/google/callback", tags=["Autenticação"])
async def google_callback(code: str, state: str):
    """Callback do Google OAuth2"""
    try:
        logger.debug(f"Recebido código de autorização: {code[:10]}...")
        
        # Troca o código pelo token
        token_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI
        }
        
        logger.debug(f"Enviando requisição para {GOOGLE_TOKEN_URL}")
        logger.debug(f"Client ID: {GOOGLE_CLIENT_ID}")
        logger.debug(f"Redirect URI: {GOOGLE_REDIRECT_URI}")
        
        async with httpx.AsyncClient() as client:
            # Obtém o token do Google
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data=token_data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            
            logger.debug(f"Resposta do Google: Status {token_response.status_code}")
            logger.debug(f"Resposta do Google: {token_response.text}")
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao trocar código por token: {token_response.text}"
                )
            
            token_json = token_response.json()
            
            if "access_token" not in token_json:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token de acesso não encontrado na resposta"
                )
            
            # Obtém informações do usuário
            headers = {"Authorization": f"Bearer {token_json['access_token']}"}
            userinfo_response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
            
            if userinfo_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao obter informações do usuário: {userinfo_response.text}"
                )
            
            user_info = userinfo_response.json()
            
            # Redireciona para a página inicial com os parâmetros
            params = {
                'message': 'auth_success',
                'token_info': json.dumps(token_json)
            }
            redirect_url = f"/?{urlencode(params)}"
            return RedirectResponse(url=redirect_url)
            
    except Exception as e:
        logger.error(f"Erro no callback: {str(e)}")
        return RedirectResponse(url="/?error=auth_failed")

@app.get("/api/auth/me", tags=["Autenticação"])
async def get_me():
    """Obtém informações do usuário autenticado"""
    return {"message": "Informações do usuário"}

@app.get("/api/auth/phone", tags=["Autenticação"])
async def phone_auth():
    """Rota para autenticação com telefone (mock)"""
    return JSONResponse({"message": "Autenticação com telefone será implementada"})

# Rotas protegidas
@app.get("/api/protected", tags=["Protegido"])
async def protected_route(current_user: dict = Depends(get_current_user)):
    """Rota protegida que requer autenticação"""
    try:
        return {
            "message": "Acesso permitido!",
            "user": {
                "id": current_user.get("id"),
                "email": current_user.get("email"),
                "name": current_user.get("name"),
                "picture": current_user.get("picture")
            }
        }
    except Exception as e:
        logger.error(f"Erro na rota protegida: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar requisição: {str(e)}"
        )

@app.post("/api/auth/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Realiza o logout do usuário"""
    try:
        # Remove qualquer prefixo 'Bearer' se existir
        token = credentials.credentials
        if token.startswith('"') and token.endswith('"'):
            token = token[1:-1]
        if token.startswith('Bearer '):
            token = token[7:]

        # Revoga o token no Google
        revoke_url = f"https://oauth2.googleapis.com/revoke?token={token}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                revoke_url,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                return {"message": "Logout realizado com sucesso"}
            else:
                logger.error(f"Erro ao revogar token: {response.status_code} - {response.text}")
                # Mesmo se houver erro, informamos sucesso ao cliente
                # pois o token pode já estar expirado
                return {"message": "Logout realizado com sucesso"}
                
    except Exception as e:
        logger.error(f"Erro no logout: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar logout"
        )

# Customização do OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="PsiCollab API",
        version="0.1.0",
        description="API para o sistema PsiCollab de assistência na elaboração de laudos psicológicos",
        routes=app.routes,
    )
    
    # Adiciona as tags
    openapi_schema["tags"] = [
        {
            "name": "Sistema",
            "description": "Operações do sistema"
        },
        {
            "name": "Autenticação",
            "description": "Operações de autenticação"
        },
        {
            "name": "Protegido",
            "description": "Rotas que requerem autenticação"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    logger.info("Iniciando servidor PsiCollab...")
    uvicorn.run(app, host="0.0.0.0", port=8080) 
"""
Gerenciamento de autenticação com Google OAuth2
"""
from typing import Optional, Union
import jwt
import time
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient, HTTPError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import GoogleUser, UserCreate, TokenData
from app.core.sms_auth import validate_phone_token

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token", auto_error=False)

# Logger
logger = logging.getLogger(__name__)

async def get_google_auth_url() -> str:
    """
    Gera a URL para autenticação com Google
    """
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    
    # Constrói a query string
    query_string = "&".join(f"{key}={value}" for key, value in params.items())
    return f"{GOOGLE_AUTH_URL}?{query_string}"

async def get_google_token(code: str) -> dict:
    """
    Obtém o token de acesso do Google usando o código de autorização
    """
    async with AsyncClient() as client:
        try:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            logger.error(f"Erro ao obter token do Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao obter token do Google"
            ) from e

async def get_google_user_info(access_token: str) -> dict:
    """
    Obtém informações do usuário do Google usando o token de acesso
    """
    async with AsyncClient() as client:
        try:
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            logger.error(f"Erro ao obter informações do usuário do Google: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao obter informações do usuário"
            ) from e

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT para o usuário
    """
    to_encode = data.copy()
    
    # Define o tempo de expiração
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire.timestamp()})
    
    # Codifica o token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt

async def process_google_user(user_info: dict, db: Session) -> User:
    """
    Processa um usuário autenticado via Google.
    Cria o usuário se não existir ou atualiza se já existe.
    """
    # Converte para o schema do GoogleUser para validação
    google_user = GoogleUser(**user_info)
    
    # Verifica se o usuário já existe pelo Google ID
    user = UserRepository.get_by_google_id(db, google_user.id)
    
    # Se não existir pelo Google ID, tenta pelo email
    if not user:
        user = UserRepository.get_by_email(db, google_user.email)
    
    # Se usuário existir, atualiza informações
    if user:
        user = UserRepository.update(
            db, 
            user,
            google_id=google_user.id,
            first_name=google_user.given_name or google_user.name.split()[0] if google_user.name else None,
            last_name=google_user.family_name or " ".join(google_user.name.split()[1:]) if google_user.name and len(google_user.name.split()) > 1 else None,
            profile_picture=google_user.picture
        )
    else:
        # Cria novo usuário
        user_data = UserCreate(
            email=google_user.email,
            nome=google_user.name,
            google_id=google_user.id,
            foto_perfil=google_user.picture,
            ativo=True
        )
        user = UserRepository.create(db, user_data)
    
    return user

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> Union[User, dict]:
    """
    Obtém o usuário atual a partir do token JWT
    Suporta tanto tokens do Google quanto tokens de telefone
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Primeiro tenta validar como token de telefone
    phone_number = validate_phone_token(token)
    if phone_number:
        return {"type": "phone", "phone_number": phone_number}

    # Se não for token de telefone, tenta validar como token Google
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("email")
        exp: int = payload.get("exp")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if exp < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"type": "google", "email": email}

    except jwt.PyJWTError as e:
        logger.error(f"Erro ao decodificar token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
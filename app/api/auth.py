"""
Módulo de autenticação da API.
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import (
    create_access_token,
    get_current_active_user,
    verify_password
)
from app.schemas.user import Token, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["autenticação"]
)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Autentica um usuário e retorna um token JWT.
    
    Args:
        form_data: Formulário com email e senha
    
    Returns:
        Token JWT
    
    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    # TODO: Implementar verificação de usuário no banco de dados
    # Por enquanto, usando um usuário de teste
    test_user = {
        "email": "teste@example.com",
        "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LcdYxEWIWQgL.IzFm"  # teste123
    }
    
    user = test_user if form_data.username == test_user["email"] else None
    if not user or not verify_password(form_data.password, user["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: dict = Depends(get_current_active_user)
) -> Any:
    """
    Retorna informações do usuário atual.
    
    Args:
        current_user: Usuário atual obtido do token JWT
    
    Returns:
        Dados do usuário
    """
    # TODO: Implementar busca de usuário no banco de dados
    # Por enquanto, retornando dados de teste
    return {
        "id": "1",
        "email": current_user["email"],
        "nome": "Usuário Teste",
        "crp": "12/3456",
        "telefone": "+5511999999999",
        "ativo": True,
        "created_at": "2024-04-01T00:00:00",
        "updated_at": None
    }

# TODO: Implementar endpoints de autenticação 
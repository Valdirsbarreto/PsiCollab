"""
Esquemas relacionados a usuários.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr

from .base import BaseSchema

class UserBase(BaseModel):
    """Esquema base de usuário."""
    email: EmailStr = Field(..., description="Email do usuário")
    nome: constr(min_length=2, max_length=100) = Field(..., description="Nome completo")
    crp: Optional[constr(pattern=r'^\d{2}/\d{4}$')] = Field(None, description="Número do CRP (XX/XXXX)")
    telefone: Optional[constr(pattern=r'^\+?1?\d{9,15}$')] = Field(None, description="Número de telefone")
    ativo: bool = Field(default=True, description="Status do usuário")

class UserCreate(UserBase):
    """Esquema para criação de usuário."""
    senha: constr(min_length=8) = Field(..., description="Senha do usuário")

class UserUpdate(BaseModel):
    """Esquema para atualização de usuário."""
    nome: Optional[constr(min_length=2, max_length=100)] = None
    email: Optional[EmailStr] = None
    crp: Optional[constr(pattern=r'^\d{2}/\d{4}$')] = None
    telefone: Optional[constr(pattern=r'^\+?1?\d{9,15}$')] = None
    ativo: Optional[bool] = None
    senha: Optional[constr(min_length=8)] = None

class UserInDB(UserBase, BaseSchema):
    """Esquema de usuário como armazenado no banco."""
    senha_hash: str = Field(..., description="Hash da senha")

class UserResponse(UserBase, BaseSchema):
    """Esquema de resposta de usuário."""
    pass

class Token(BaseModel):
    """Esquema de token de acesso."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Dados contidos no token JWT."""
    email: str
    exp: Optional[int] = None 
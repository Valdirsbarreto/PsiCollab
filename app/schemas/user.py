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
    foto_perfil: Optional[str] = Field(None, description="URL da foto de perfil")

class UserCreate(UserBase):
    """Esquema para criação de usuário."""
    senha: Optional[constr(min_length=8)] = Field(None, description="Senha do usuário (opcional para OAuth)")
    google_id: Optional[str] = Field(None, description="ID do usuário no Google")

class UserUpdate(BaseModel):
    """Esquema para atualização de usuário."""
    nome: Optional[constr(min_length=2, max_length=100)] = None
    email: Optional[EmailStr] = None
    crp: Optional[constr(pattern=r'^\d{2}/\d{4}$')] = None
    telefone: Optional[constr(pattern=r'^\+?1?\d{9,15}$')] = None
    ativo: Optional[bool] = None
    senha: Optional[constr(min_length=8)] = None
    foto_perfil: Optional[str] = None
    google_id: Optional[str] = None

class UserInDB(UserBase, BaseSchema):
    """Esquema de usuário como armazenado no banco."""
    senha_hash: Optional[str] = Field(None, description="Hash da senha (pode ser nulo para OAuth)")
    google_id: Optional[str] = Field(None, description="ID do usuário no Google")

class UserResponse(UserBase, BaseSchema):
    """Esquema de resposta de usuário."""
    id: str
    ativo: bool = True
    auth_provider: Optional[str] = Field(None, description="Provedor de autenticação (google, email, etc)")

class Token(BaseModel):
    """Esquema de token de acesso."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Dados contidos no token JWT."""
    email: str
    exp: Optional[int] = None
    
class GoogleUser(BaseModel):
    """Esquema para os dados do usuário retornados pelo Google."""
    id: str
    email: EmailStr
    verified_email: bool
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None 
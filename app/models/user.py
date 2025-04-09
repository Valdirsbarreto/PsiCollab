"""
Modelo de usuário para o PsiCollab.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional
import uuid

Base = declarative_base()

class User(Base):
    """
    Modelo de usuário para armazenamento no banco de dados.
    Armazena informações básicas de usuário e dados de autenticação OAuth2.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    
    # Dados de autenticação OAuth2
    google_id = Column(String, unique=True, nullable=True, index=True)
    
    # Campos para controle
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.email}>" 
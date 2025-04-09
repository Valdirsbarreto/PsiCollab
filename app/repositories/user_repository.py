"""
Repositório para operações com usuários.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List

from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    """
    Repositório para operações com usuários no banco de dados.
    """
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """
        Cria um novo usuário no banco de dados.
        """
        db_user = User(
            email=user_data.email,
            first_name=user_data.nome.split()[0] if user_data.nome else None,
            last_name=" ".join(user_data.nome.split()[1:]) if user_data.nome and len(user_data.nome.split()) > 1 else None,
            profile_picture=user_data.foto_perfil,
            google_id=user_data.google_id
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """
        Busca um usuário pelo email.
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_google_id(db: Session, google_id: str) -> Optional[User]:
        """
        Busca um usuário pelo ID do Google.
        """
        return db.query(User).filter(User.google_id == google_id).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID.
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def update(db: Session, user: User, **kwargs) -> User:
        """
        Atualiza os dados de um usuário.
        """
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lista todos os usuários.
        """
        return db.query(User).offset(skip).limit(limit).all() 
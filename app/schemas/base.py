"""
Esquemas base para todos os modelos do sistema.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    """Esquema base com campos comuns."""
    id: Optional[str] = Field(None, description="ID único do registro")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização")
    
    class Config:
        """Configurações do modelo."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True 
"""
Módulo de API do PsiCollab.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .documents import router as documents_router
from .analysis import router as analysis_router
from .reports import router as reports_router
from .qrcode import router as qrcode_router

# Criar o router principal
api_router = APIRouter()

# Incluir todos os routers
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(documents_router)
api_router.include_router(analysis_router)
api_router.include_router(reports_router)
api_router.include_router(qrcode_router)

__all__ = [
    'auth_router',
    'users_router',
    'documents_router',
    'analysis_router',
    'reports_router',
    'qrcode_router'
] 
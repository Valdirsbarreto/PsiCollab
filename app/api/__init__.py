"""
Endpoints da API
"""

from .auth import router as auth_router
from .users import router as users_router
from .documents import router as documents_router
from .analysis import router as analysis_router
from .reports import router as reports_router
from .qrcode import router as qrcode_router

__all__ = [
    'auth_router',
    'users_router',
    'documents_router',
    'analysis_router',
    'reports_router',
    'qrcode_router'
] 
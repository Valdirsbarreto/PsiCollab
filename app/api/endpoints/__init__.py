"""
Endpoints da API REST do PsiCollab.
"""

from fastapi import APIRouter
from .search import router as search_router

# Cria o roteador principal
router = APIRouter()

# Inclui roteadores específicos
router.include_router(search_router, prefix="/search", tags=["search"]) 
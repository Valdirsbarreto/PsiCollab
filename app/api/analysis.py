"""
Módulo de rotas de análises da API.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=["análise"]
)

# TODO: Implementar rotas de análise 
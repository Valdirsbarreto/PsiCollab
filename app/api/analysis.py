"""
Módulo de rotas de análises da API.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=["análises"]
)

# TODO: Implementar endpoints de análises 
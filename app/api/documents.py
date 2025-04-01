"""
Módulo de rotas de documentos da API.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["documentos"]
)

# TODO: Implementar endpoints de documentos 
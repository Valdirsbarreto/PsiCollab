"""
Rotas relacionadas a documentos.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["documentos"]
)

# TODO: Implementar rotas de documentos 
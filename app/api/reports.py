"""
Módulo de rotas de relatórios da API.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/reports",
    tags=["relatórios"]
)

# TODO: Implementar endpoints de relatórios 
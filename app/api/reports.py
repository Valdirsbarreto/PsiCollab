"""
Rotas relacionadas a relatórios.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/reports",
    tags=["relatórios"]
)

# TODO: Implementar rotas de relatórios 
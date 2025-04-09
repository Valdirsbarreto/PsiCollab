"""
Rotas relacionadas a usuários.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["usuários"]
)

# TODO: Implementar rotas de usuários 
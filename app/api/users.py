"""
Módulo de rotas de usuários da API.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["usuários"]
)

# TODO: Implementar endpoints de usuários 
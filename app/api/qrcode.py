"""
Módulo de rotas de QR codes da API.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/qrcode",
    tags=["qr codes"]
)

# TODO: Implementar endpoints de QR codes 
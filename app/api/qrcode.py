"""
Rotas relacionadas a QR Code.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/qrcode",
    tags=["qrcode"]
)

# TODO: Implementar rotas de QR Code 
"""
Script para executar o servidor da API.
"""
import argparse
import logging
import uvicorn
from app.core.config import settings

# Configuração de logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def run_api(host: str = "0.0.0.0", port: int = 8000, reload: bool = False) -> None:
    """
    Executa o servidor da API.
    
    Args:
        host: Host para o servidor
        port: Porta para o servidor
        reload: Se deve recarregar automaticamente ao detectar mudanças
    """
    logger.info(f"Iniciando servidor API em {host}:{port}")
    
    # Configuração do Uvicorn
    uvicorn_config = {
        "app": "app.main:app",
        "host": host,
        "port": port,
        "reload": reload,
        "log_level": settings.LOG_LEVEL.lower(),
        "workers": 1
    }
    
    # Iniciar o servidor
    uvicorn.run(**uvicorn_config)

def main():
    """
    Função principal do script.
    """
    parser = argparse.ArgumentParser(description="Executa o servidor da API")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host para o servidor"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Porta para o servidor"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Recarregar automaticamente ao detectar mudanças"
    )
    
    args = parser.parse_args()
    run_api(args.host, args.port, args.reload)

if __name__ == "__main__":
    main() 
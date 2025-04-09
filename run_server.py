"""
Script para iniciar o servidor FastAPI do PsiCollab.
"""
import os
import sys
import uvicorn
import logging
from app.core.config import settings
import subprocess

# Configuração do logger
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.LOG_FILE, 'a')
    ]
)
logger = logging.getLogger(__name__)

def create_log_dir():
    """Cria o diretório de logs se não existir."""
    log_dir = os.path.dirname(settings.LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        logger.info(f"Diretório de logs criado: {log_dir}")

def main():
    print("Iniciando servidor PsiCollab...")
    
    # Comando para executar o uvicorn diretamente
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "psicollab_app:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8080",
        "--reload"
    ]
    
    try:
        # Executa o processo e mantém o terminal aberto
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print(f"Servidor iniciado! Acesse: http://127.0.0.1:8080/docs")
        print("Pressione Ctrl+C para encerrar...")
        
        # Mostra a saída do servidor em tempo real
        for line in process.stdout:
            print(line, end='')
            
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
        process.terminate()
        
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
        
if __name__ == "__main__":
    main() 
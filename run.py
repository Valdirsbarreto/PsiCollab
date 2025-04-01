"""
Script de inicialização do PsiCollab.
"""
import os
import sys
import socket
import logging
import uvicorn
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_port_available(host: str, port: int) -> bool:
    """Verifica se a porta está disponível."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except socket.error:
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    dependencies = [
        'fastapi',
        'pydantic',
        'jose',
        'passlib',
        'uvicorn',
        'python-multipart',
        'email-validator'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            logger.info(f"✓ {dep} instalado")
        except ImportError as e:
            logger.error(f"✗ {dep} não encontrado: {str(e)}")
            return False
    return True

def check_environment():
    """Verifica se o ambiente está configurado corretamente."""
    # Verificar Python path
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
        logger.info(f"Adicionado {current_dir} ao PYTHONPATH")
    
    # Verificar arquivo .env
    env_file = current_dir / '.env'
    if not env_file.exists():
        logger.error(f"Arquivo .env não encontrado em {env_file}")
        return False
    
    # Verificar variáveis de ambiente
    required_vars = ['OPENAI_API_KEY', 'SECRET_KEY']
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            logger.error(f"Variável de ambiente {var} não configurada")
        else:
            logger.info(f"✓ {var} configurado")
    
    return True

def main():
    """Função principal de inicialização."""
    try:
        logger.info("Iniciando verificações do ambiente...")
        
        # Verificar dependências
        if not check_dependencies():
            logger.error("Falha na verificação de dependências")
            sys.exit(1)
        
        # Verificar ambiente
        if not check_environment():
            logger.warning("Ambiente não está completamente configurado")
        
        # Configurar o servidor
        host = "127.0.0.1"  # Usando IP explícito em vez de localhost
        port = 8000
        
        # Verificar se a porta está disponível
        if not check_port_available(host, port):
            logger.error(f"Porta {port} já está em uso!")
            sys.exit(1)
        
        config = {
            "app": "app.main:app",
            "host": host,
            "port": port,
            "reload": True,
            "workers": 1,
            "log_level": "debug",
            "access_log": True,
            "use_colors": True,
            "reload_dirs": [str(Path(__file__).parent / "app")],
            "factory": False,
            "timeout_keep_alive": 0,
        }
        
        # Iniciar o servidor
        logger.info(f"Iniciando servidor em http://{host}:{port}")
        logger.info("Pressione CTRL+C para parar o servidor")
        uvicorn.run(**config)
        
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {str(e)}")
        logger.exception(e)  # Isso irá mostrar o traceback completo
        sys.exit(1)

if __name__ == "__main__":
    main() 
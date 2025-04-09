import subprocess
import time
import sys
import requests
import logging
from typing import Tuple

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_docker() -> bool:
    """Verifica se o Docker está rodando."""
    try:
        subprocess.run(["docker", "info"], capture_output=True, check=True)
        logger.info("✅ Docker está rodando")
        return True
    except subprocess.CalledProcessError:
        logger.error("❌ Docker não está rodando. Por favor, inicie o Docker Desktop")
        return False

def check_service(url: str, name: str, timeout: int = 30) -> bool:
    """Verifica se um serviço está respondendo."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info(f"✅ {name} está rodando em {url}")
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
        logger.info(f"⏳ Aguardando {name} iniciar... ({int(time.time() - start_time)}s)")
    
    logger.error(f"❌ {name} não respondeu após {timeout} segundos")
    return False

def start_services() -> Tuple[subprocess.Popen, bool]:
    """Inicia os serviços usando docker-compose."""
    try:
        logger.info("🚀 Iniciando serviços...")
        process = subprocess.Popen(
            ["docker", "compose", "up", "--build"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return process, True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erro ao iniciar serviços: {e}")
        return None, False

def main():
    """Função principal de inicialização."""
    logger.info("🔄 Iniciando verificações do sistema...")

    # Verifica se o Docker está rodando
    if not check_docker():
        return

    # Inicia os serviços
    process, success = start_services()
    if not success:
        return

    # Verifica se os serviços estão respondendo
    services_ok = True
    services_ok &= check_service("http://localhost:8080/health", "API")
    services_ok &= check_service("http://localhost:6333", "Qdrant")

    if services_ok:
        logger.info("""
✨ PsiCollab iniciado com sucesso! ✨

📌 Serviços disponíveis:
   • Interface Web: http://localhost:8080
   • API Docs: http://localhost:8080/docs
   • Qdrant: http://localhost:6333

💡 Para parar os serviços, pressione Ctrl+C
""")
        
        # Mantém o script rodando e mostra os logs
        try:
            for line in process.stdout:
                print(line, end='')
        except KeyboardInterrupt:
            logger.info("\n🛑 Encerrando serviços...")
            subprocess.run(["docker", "compose", "down"])
            logger.info("👋 Serviços encerrados. Até logo!")

if __name__ == "__main__":
    main() 
@echo off
echo ========================================
echo    Iniciando PsiCollab com Docker
echo ========================================

REM Verifica se o Docker está rodando
docker info > nul 2>&1
if errorlevel 1 (
    echo [X] Docker nao esta rodando!
    echo [!] Por favor, inicie o Docker Desktop primeiro
    pause
    exit /b
)
echo [✓] Docker esta rodando

REM Inicia os serviços
echo [*] Iniciando servicos...
docker compose up --build

REM O script continuará rodando até ser interrompido com Ctrl+C
echo.
echo Para encerrar os servicos, pressione Ctrl+C
pause 
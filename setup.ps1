# Script de configuração do ambiente PsiCollab

# Criar e ativar ambiente virtual
Write-Host "Criando ambiente virtual..." -ForegroundColor Green
python -m venv venv
.\venv\Scripts\Activate

# Atualizar pip
Write-Host "Atualizando pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Green
pip install -r requirements.txt

# Verificar instalação do uvicorn
Write-Host "Verificando instalação do uvicorn..." -ForegroundColor Green
pip show uvicorn

# Criar arquivo .env se não existir
if (-not (Test-Path .env)) {
    Write-Host "Criando arquivo .env..." -ForegroundColor Green
    @"
# Configurações do Ambiente
DEBUG=True
ENVIRONMENT=development

# Chaves de API
OPENAI_API_KEY=sua_chave_aqui
SECRET_KEY=chave-secreta-temporaria

# Configurações do Banco de Dados
VECTOR_DB_URL=http://localhost:6333
"@ | Out-File -FilePath .env -Encoding UTF8
}

Write-Host "Configuração concluída!" -ForegroundColor Green
Write-Host "Para iniciar o servidor, execute: python run.py" -ForegroundColor Yellow 
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="PsiCollab API",
    description="API para o sistema PsiCollab de assistência na elaboração de laudos psicológicos",
    version="0.1.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas do sistema
@app.get("/health", tags=["Sistema"])
async def health_check():
    """
    Verificação de saúde da API
    """
    return {"status": "online"}

@app.get("/", tags=["Sistema"])
async def root():
    """
    Rota principal - Retorna a página de login
    """
    return {"message": "Bem-vindo ao PsiCollab API"}

# Rotas de autenticação
@app.get("/api/auth/google", tags=["Autenticação"])
async def google_auth():
    """
    Inicia o fluxo de autenticação com Google
    """
    return {"message": "Rota de autenticação Google"}

@app.get("/api/auth/callback", tags=["Autenticação"])
async def google_callback(code: str = "default_code"):
    """
    Callback do Google OAuth2
    """
    return {"message": "Rota de callback Google", "code": code}

@app.get("/api/auth/me", tags=["Autenticação"])
async def get_me():
    """
    Obtém informações do usuário autenticado
    """
    return {"message": "Informações do usuário"}

@app.get("/api/auth/phone", tags=["Autenticação"])
async def phone_auth():
    """
    Rota para autenticação com telefone (mock)
    """
    return JSONResponse({"message": "Autenticação com telefone será implementada"})

# Rotas protegidas
@app.get("/api/protected", tags=["Protegido"])
async def protected_route():
    """
    Exemplo de rota protegida
    """
    return {"message": "Rota protegida"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003) 
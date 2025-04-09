from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI(
    title="Simple Router Test",
    description="Teste simples de routers com FastAPI",
    version="0.1.0"
)

# Criação dos routers
system_router = APIRouter(
    prefix="",
    tags=["Sistema"]
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@system_router.get("/")
async def root():
    """Rota raiz"""
    return {"message": "Hello from root"}

@system_router.get("/health")
async def health():
    """Verificação de saúde"""
    return {"status": "OK"}

@auth_router.get("/login")
async def login():
    """Login endpoint"""
    return {"message": "Login page"}

# Incluindo os routers
app.include_router(system_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002) 
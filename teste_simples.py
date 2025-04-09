from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Teste API",
    description="API de teste simples",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/", tags=["root"])
async def root():
    """Rota raiz"""
    return {"message": "Hello World"}

@app.get("/teste", tags=["teste"])
async def teste():
    """Rota de teste"""
    return {"message": "Esta é uma rota de teste"}

@app.get("/health", tags=["sistema"])
async def health():
    """Verificação de saúde"""
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8090) 
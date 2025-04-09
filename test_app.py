from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Teste API",
    description="API de teste para verificar o Swagger UI",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Rota principal"""
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """Rota de exemplo com parâmetro"""
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(name: str):
    """Rota de exemplo com POST"""
    return {"name": name}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) 
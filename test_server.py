from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Servidor FastAPI funcionando"}

if __name__ == "__main__":
    print("Iniciando servidor na porta 8000...")
    uvicorn.run(
        "test_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

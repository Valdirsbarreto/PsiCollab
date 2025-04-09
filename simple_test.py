from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    print("Servidor iniciando em http://localhost:3000")
    uvicorn.run(
        app,
        host="localhost",
        port=3000,
        log_level="info"
    ) 
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    print("Iniciando servidor em http://localhost:7000")
    uvicorn.run(
        app,
        host="localhost",  # Usando apenas localhost
        port=7000,
        reload=True,
        access_log=True,
        log_level="debug"
    ) 
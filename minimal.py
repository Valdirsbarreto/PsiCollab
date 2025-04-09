from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def health():
    return {"status": "online"}

@app.get("/api/auth/google")
def auth_google():
    return {"message": "Google auth endpoint"}

# Para executar: uvicorn minimal:app --reload 
"""
Servidor da API PsiCollab.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="debug",
        workers=1
    ) 
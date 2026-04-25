from fastapi import FastAPI
from routes import auth, clientes

app = FastAPI()
app.include_router(auth.router)
app.include_router(clientes.router)


@app.get("/")
def home():
    return {"message": "Página inicial da API de Clientes"}

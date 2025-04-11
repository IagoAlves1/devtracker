from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return{"mensagem": "API funcionando!"}
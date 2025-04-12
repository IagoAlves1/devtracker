from fastapi import FastAPI
from api.v1.endpoints import user

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando!"}

app.include_router(user.router, prefix="/api/v1/endpoints")
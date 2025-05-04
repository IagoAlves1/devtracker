from fastapi import FastAPI
from api.v1.endpoints import user, auth
from init_db import create_master_admin
from core.database import SessionLocal

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando!"}

app.include_router(user.router, prefix="/api/v1/endpoints")
app.include_router(auth.router, prefix="/api/v1/endpoints/auth")

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    create_master_admin(db)
    db.close()
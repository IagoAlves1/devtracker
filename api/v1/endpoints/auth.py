from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import SessionLocal
from services.user_service import get_user_by_email
from core.security import create_token_access, get_current_user
from core.hashing import verify_password

from models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", summary="Login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    usuario = get_user_by_email(db, form_data.username)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
     
    if not verify_password(form_data.password, usuario.password):
        raise HTTPException(status_code=400, detail="Senha incorreta")
     
    dados_token = {"sub": usuario.email}
    token = create_token_access(dados_token)

    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected-route", summary="Validar se usuário está logado")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Login realizado com sucesso! Bem-vindo, {current_user.name}!"}
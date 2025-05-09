from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import SessionLocal
from services.user_service import get_user_by_email
from core.security import create_token_access, get_current_user
from core.hashing import verify_password
from utils.logger import logger
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
        logger.error(f"Tentativa de login com e-mail inexistente: {form_data.username}")
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
     
    if not verify_password(form_data.password, usuario.password):
        logger.error(f"Senha incorreta para e-mail: {form_data.username}")
        raise HTTPException(status_code=400, detail="Senha incorreta")
     
    dados_token = {"sub": usuario.email}
    token = create_token_access(dados_token)
    logger.info(f"Login bem-sucedido para usuário: {usuario.id} - {usuario.email}")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected-route", summary="Validar se usuário está logado")
def protected_route(current_user: User = Depends(get_current_user)):
    if get_current_user is None:
        logger.error("Tentativa de acesso a recurso protegido sem autenticação válida.")
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    logger.info(f"Acesso à rota protegida autorizado para usuário: {current_user.id} - {current_user.email}")
    return {"message": f"Login realizado com sucesso! Bem-vindo, {current_user.name}!"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, update_user, delete_user, list_users
from schemas.user import UserCreate, UserResponse, UserUpdate
from core.database import Sessionlocal
from typing import List, Optional

router = APIRouter()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/user/{user_id}", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    if user.name == "":
        raise HTTPException(status_code=400, detail="Nome não pode ser vazio, preencha seu nome no campo Nome e tente novamente!")
    elif user.password == "":
        raise HTTPException(status_code=400, detail="Senha senha não pode ser vazia, digite a senha criada no campo Senha e tente novamente!")
    return create_user(db=db, user=user)

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session =  Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não enconstrado")
    return db_user

@router.put("/user/{user_id}")
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não enconstrado")
    return db_user

@router.delete("/user/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não enconstrado")
    return {"message": "Usuário deletado com sucesso"}

@router.get("/users/", response_model=List[UserResponse])
def list_users_endpoint(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session =  Depends(get_db)):

    return list_users(db=db, skip=skip, limit=limit, name=name, email=email)
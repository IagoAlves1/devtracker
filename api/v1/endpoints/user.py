from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, update_user, delete_user, list_users, patch_user
from schemas.user import UserCreate, UserResponse, UserUpdate, UserPatch
from core.database import Sessionlocal
from typing import List, Optional
from models.user import User
from core.security import get_current_user

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
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user_id).first()    
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este usuário.")

    if user.password:
        from core.hashing import create_hash
        user.password = create_hash(user.password)

    updated_user = update_user(db=db, user_id=user_id, user_data=user)
    
    return {"message": "Usuário atualizado com sucesso"}

@router.delete("/user/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este usuário.")
    
    user = db.query(User).filter(User.id == user_id).first()
   
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuário excluído com sucesso"}
    
@router.get("/users/", response_model=List[UserResponse])
def list_users_endpoint(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)):

    return list_users(db=db, skip=skip, limit=limit, name=name, email=email)

@router.patch("/users/{user_id}")
def update_user_partially(user_id: int, user_patch: UserPatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = patch_user(db, user_id, user_patch, current_user)
    return updated_user
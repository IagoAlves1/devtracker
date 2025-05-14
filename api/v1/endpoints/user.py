from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, update_user, list_users, patch_user, deactivate_user, activate_user, promote_user_to_admin, delete_user, get_data_current_user
from schemas.user import UserCreate, UserResponse, UserUpdate, UserPatch
from core.database import SessionLocal
from typing import List, Optional
from models.user import User
from core.security import get_current_user
from core.dependencies import is_admin
from utils.logger import logger

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/user/{user_id}", response_model=UserResponse, summary="Criar um usuário")
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/user/{user_id}", response_model=UserResponse, summary="Busca de usuário por ID")
def get_user_endpoint(user_id: int, db: Session =  Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user(user_id=user_id, db=db, current_user=current_user)

@router.put("/user/{user_id}", summary="Atualizar todas as informações de um usuário")
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):  
    return update_user(db=db, user_id=user_id, user_data=user, current_user=current_user)

@router.delete("/user/{user_id}", summary="Deletar usuário")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_user(user_id, db, current_user)

@router.get("/users/", response_model=List[UserResponse], summary="Listar usuários")
def list_users_endpoint(skip: int = 0, limit: int = 10, name: Optional[str] = None, email: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_users(db=db, skip=skip, limit=limit, name=name, email=email)

@router.patch("/users/{user_id}", summary="Atualizar parcialmente dados do usuário")
def update_user_partially(user_id: int, user_patch: UserPatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_user(db=db, user_id=user_id, user_patch=user_patch, current_user=current_user )

@router.patch("/users/{user_id}", summary="Promover usuário a admin")
def promote_user_to_admin_endpoint(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return promote_user_to_admin(user_id, current_user, db)

@router.get("/users/{user_id}", response_model=UserResponse, summary="Meus dados")
def get_data_current_user_endpoint(current_user: User = Depends(get_current_user)):
    return get_data_current_user(current_user=current_user)

@router.patch("/users/{user_id}/deactivate", summary="Desativar usuário")
def deactivate_user_route(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return deactivate_user(user_id, current_user, db)

@router.patch("/users/{user_id}/activate", summary="Ativar usuário")
def activate_user_route_endpoint(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return activate_user(user_id, current_user, db)

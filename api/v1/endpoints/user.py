from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user, update_user, list_users, patch_user
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
    if user.name == "":
        logger.error(f"Erro ao criar usuário: {user.email}")
        raise HTTPException(status_code=400, detail="Nome não pode ser vazio, preencha seu nome no campo Nome e tente novamente!")
    elif user.password == "":
        logger.error(f"Erro ao criar usuário: {user.name}")
        raise HTTPException(status_code=400, detail="Senha senha não pode ser vazia, digite a senha criada no campo Senha e tente novamente!")
    logger.info(f"Usuário criado com sucesso - ID: {create_user.id}, E-mail: {create_user.email}")
    return create_user(db=db, user=user)


@router.get("/user/{user_id}", response_model=UserResponse, summary="Busca de usuário por ID")
def get_user_endpoint(user_id: int, db: Session =  Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        logger.error(f"Erro ao localizar usuário - ID: {user_id.id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    logger.info(f"Usuário localizado com sucesso - ID: {user_id}")
    return db_user

@router.put("/user/{user_id}", summary="Atualizar todas as informações de um usuário")
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user_id).first()    
    if db_user is None:
        logger.error("Erro ao localizar usuário id: {user_id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if current_user.id != user_id:
        logger.error(f"Permissão negada: Usuário {current_user.id} tentou atualizar o usuário {user_id}")
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este usuário.")

    if user.password:
        from core.hashing import create_hash
        user.password = create_hash(user.password)

    updated_user = update_user(db=db, user_id=user_id, user_data=user)
    logger.info(f"Usuário atualizado com sucesso - ID: {user_id}")
    return {"message": "Usuário atualizado com sucesso"}

@router.delete("/user/{user_id}", summary="Deletar usuário")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role == "admin" and current_user.id == user_id:
        logger.error("Operação negada: administrador tentou excluir a si mesmo")
        raise HTTPException(status_code=403, detail="Admins não podem excluir a si mesmos.")

    if current_user.role != "admin" and current_user.id != user_id:
        logger.error(f"Usuário {current_user.id} tentou excluir outro usuário sem permissão")
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este usuário.")
    
    if current_user.role == "admin" and user.role == "admin" and current_user.id != user_id:
        logger.error("Operação negada: um administrador tentou excluir outro administrador")
        raise HTTPException(status_code=403, detail="Você não pode excluir outro administrador.")
    
    user = db.query(User).filter(User.id == user_id).first()
   
    if not user:
        logger.error(f"Usuário não encontrado para exclusão - ID: {user.id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    logger.info(f"Usuário deletado com sucesso - ID: {user_id}")
    db.delete(user)
    db.commit()
    return {"message": "Usuário excluído com sucesso"}
    
@router.get("/users/", response_model=List[UserResponse], summary="Listar usuários")
def list_users_endpoint(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db)):

    logger.info("Iniciada listagem de usuários")
    return list_users(db=db, skip=skip, limit=limit, name=name, email=email)

@router.patch("/users/{user_id}", summary="Atualizar parcialmente dados do usuário")
def update_user_partially(user_id: int, user_patch: UserPatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = patch_user(db, user_id, user_patch, current_user)
    if not user_id:
        logger.error(f"Erro ao localizar usuário - ID: {user_id.id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if user_id.id != current_user.id:
        logger.error(f"Permissão negada: usuário {current_user.id} tentou atualizar os dados do usuário {user_id}")
        raise HTTPException(status_code=403, detail="Acesso negado")
    logger.info(f"Usuário atualizado com sucesso - ID: {user_id}")
    return updated_user

@router.patch("/users/{user_id}", summary="Promover usuário a admin")
def promote_user_to_admin(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if current_user.role != "admin":
        logger.error(f"Usuário {current_user.id} tentou se promover para administrador (operação negada)")
        raise HTTPException(status_code=403, detail="Apenas admins podem promover outros usuários a admin")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error("Usuário não encontrado na tentativa de promoção para administrador")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.role == "admin":
        logger.error("Tentativa inválida: usuário já é administrador")
        return {"message":  "Usuário já é admin"}
    
    user.role = "admin"
    db.commit()
    logger.info(f"Usuário promovido a administrador - ID: {user_id}")
    return {"message": f"Usuário '{user.name}' promovido a admin com sucesso"}

@router.get("/users/{user_id}", response_model=UserResponse, summary="Meus dados")
def get_data_current_user(current_user: User = Depends(get_current_user)):
    
    if current_user is not None:
        logger.info("Consulta de dados do usuário logado realizada com sucesso")
        return current_user
    logger.error("Usuário não encontrado durante consulta de dados do usuário logado")
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
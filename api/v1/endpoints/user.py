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
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(status_code=400, detail="Nome não pode ser vazio, preencha seu nome no campo Nome e tente novamente!")
    elif user.password == "":
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(status_code=400, detail="Senha senha não pode ser vazia, digite a senha criada no campo Senha e tente novamente!")
    logger.info(f"Usuário criado: {create_user.id} - {create_user.email}")
    return create_user(db=db, user=user)



@router.get("/user/{user_id}", response_model=UserResponse, summary="Busca de usuário por ID")
def get_user_endpoint(user_id: int, db: Session =  Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        logger.error("Erro ao localizar usuário id: {user.id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    logger.info("Sucesso na busca de usuário")
    return db_user

@router.put("/user/{user_id}", summary="Atualizar todas as informações de um usuário")
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user_id).first()    
    if db_user is None:
        logger.error("Erro ao localizar usuário id: {user_id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if current_user.id != user_id:
        logger.error("Permissão de usuário {current_user.id} para atualizar usuário {user_id} negada")
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este usuário.")

    if user.password:
        from core.hashing import create_hash
        user.password = create_hash(user.password)

    updated_user = update_user(db=db, user_id=user_id, user_data=user)
    logger.info("Usuário: {user_id}, atualizado")
    return {"message": "Usuário atualizado com sucesso"}

@router.delete("/user/{user_id}", summary="Deletar usuário")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role == "admin" and current_user.id == user_id:
        logger.error("Um administrador tentou excluir a si mesmo, operação não permitida")
        raise HTTPException(status_code=403, detail="Admins não podem excluir a si mesmos.")

    if current_user.role != "admin" and current_user.id != user_id:
        logger.error("Usuário id: {current_user.id}, tentou excluir outro usuário")
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este usuário.")
    
    if current_user.role == "admin" and user.role == "admin" and current_user.id != user_id:
        logger.error("Um administrador tentou excluir outro administrador")
        raise HTTPException(status_code=403, detail="Você não pode excluir outro administrador.")
    
    user = db.query(User).filter(User.id == user_id).first()
   
    if not user:
        logger.error("Usuário id: {user.id}, não encontrado")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    logger.info("Usuário id: {user_id}, foi deletado")
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

    logger.info("Chamada função listagem de usuários")
    return list_users(db=db, skip=skip, limit=limit, name=name, email=email)

@router.patch("/users/{user_id}", summary="Atualizar parcialmente dados do usuário")
def update_user_partially(user_id: int, user_patch: UserPatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = patch_user(db, user_id, user_patch, current_user)
    logger.info("Usuário id: {user_id}, foi atualizado")
    return updated_user

@router.patch("/users/{user_id}", summary="Promover usuário a admin")
def promote_user_to_admin(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if current_user.role != "admin":
        logger.error("Usuário id: {current_user.id}, tentou promover a si mesmo para administrador")
        raise HTTPException(status_code=403, detail="Apenas admins podem promover outros usuários a admin")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error("Usuário não encontrado na chamada da função para promover usuários a administrador")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.role == "admin":
        logger.error("Houve tentativa de promover um usuário administrador para administrador")
        return {"message":  "Usuário já é admin"}
    
    user.role = "admin"
    db.commit()
    logger.info("Usuário id: {user_id}, foi promovido a administrador")
    return {"message": f"Usuário '{user.name}' promovido a admin com sucesso"}

@router.get("/users/{user_id}", response_model=UserResponse, summary="Meus dados")
def get_data_current_user(current_user: User = Depends(get_current_user)):
    
    if current_user is not None:
        logger.info("Realizado consulta de dados de usuário logado")
        return current_user
    logger.error("Usuário não encontrado na chamada de função buscar dados do usuário logado")
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
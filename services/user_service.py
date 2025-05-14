from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserPatch
from core.hashing import create_hash
from typing import Optional
from pydantic import EmailStr
from fastapi import HTTPException
from utils.logger import logger

def create_user(db: Session, user: UserCreate):
    hashed_pw = create_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_pw, role="user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_data: UserUpdate, current_user: User):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("Usuário não encontrado durante a desativação de usuário")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if current_user.role != "admin" or current_user.id != user.id:
        logger.error(f"Permissão negada: Usuário {current_user.id} tentou atualizar o usuário {user_id}")
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este usuário.")

    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        user.email = user_data.email

    if user_data.password is not None:
        from core.hashing import create_hash
        user.password = create_hash(user_data.password)

    db.commit()
    db.refresh(user)
    logger.info(f"Usuário atualizado com sucesso - ID: {user_id}")
    return {"message": "Usuário atualizado com sucesso"}

def delete_user(user_id: int, db: Session, current_user: User):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error(f"Usuário não encontrado para exclusão - ID: {user.id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    if current_user.role == "admin" and user.id == current_user.id:
        logger.error("Operação negada: administrador tentou excluir a si mesmo")
        raise HTTPException(status_code=403, detail="Admins não podem excluir a si mesmos.")

    if current_user.role != "admin" and current_user.id != user_id:
        logger.error(f"Usuário {current_user.id} tentou excluir outro usuário sem permissão")
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este usuário.")
    
    if current_user.role == "admin" and user.role == "admin" and current_user.id != user.id:
        logger.error("Operação negada: um administrador tentou excluir outro administrador")
        raise HTTPException(status_code=403, detail="Você não pode excluir outro administrador.")
  
    db.delete(user)
    db.commit()
    logger.info(f"Usuário deletado com sucesso - ID: {user_id}")
    return {"message": "Usuário excluído com sucesso"}

def list_users(db: Session, skip: int = 0, limit: int = 10, name: str = None, email: str = None):
    query = db.query(User)

    if name:
        query = query.filter(User.name.contains(name))
    if email:
        query = query.filter(User.email.contains(email))
    
    return query.offset(skip).limit(limit).all()

def get_user_by_email(db: Session, user_email: EmailStr) -> Optional[User]:
    
    return db.query(User).filter(User.email == user_email).first()


def patch_user(db: Session, user_id: int, user_patch: UserPatch, current_user: User):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user_patch.name is not None:
        user.name = user_patch.name
    if user_patch.email is not None:
        user.email = user_patch.email
    if user_patch.password is not None:
        user.password = create_hash(user_patch.password)

    db.commit()
    db.refresh(user)
    return user

def activate_user(user_id: int, current_user: User, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        logger.error("Usuário não encontrado durante a desativação de usuário")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if current_user.role == "admin" or current_user.id == user.id:
            
        if user.is_active == True:
            logger.error(f"Usuário - ID:{user.id} já está ativo")
            return{"message": f"Usuário - ID: {user.id} já está ativo"}
        
        user.is_active = True
        db.commit()
        logger.info(f"Usuário - ID: {user.id} foi reativado")
        return {"message" : f"Usuário - ID: {user.id} foi reativado com sucesso!"}

    logger.error(f"Usuário - ID: {current_user.id}, teve acesso negado para recurso de ativação")
    raise HTTPException(status_code=403, detail="Acesso negado")

def deactivate_user(user_id: int, current_user: User, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if current_user is None:
        logger.error("Acesso negado a desativação de usuário")
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    if not user:
        logger.error("Usuário não encontrado durante a desativação de usuário")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.is_active == False:
        logger.error(f"Usuário - ID:{user.id} já está desativado")
        return {"message": f"Usuário {user_id} já foi desativado"}

    if current_user.role == "admin" or current_user.id == user.id:
        user.is_active = False
        db.commit()
        logger.info(f"Usuário com ID {user.id} desativado com sucesso.")
        return {"message": f"Usuário - ID: {user.id} usuário foi desativado"}
    
    if current_user.id != user_id:
            logger.error(f"Usuário - ID: {current_user.id} tentou excluir usuário - ID: {user_id}")
            raise HTTPException(status_code=403, detail="Você não tem permissão para desativar um usuário diferente do seu")
   
def promote_user_to_admin(user_id: int, current_user: User, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    
    if current_user.role != "admin":
        logger.error(f"Usuário {current_user.id} tentou se promover para administrador (operação negada)")
        raise HTTPException(status_code=403, detail="Apenas admins podem promover outros usuários a admin")
    
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

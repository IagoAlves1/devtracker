from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserPatch
from core.hashing import create_hash
from typing import Optional
from pydantic import EmailStr
from fastapi import HTTPException
from utils.logger import logger

def create_user(db: Session, user: UserCreate):
    try:
        if user.name == "":
            logger.error("Erro ao criar usuário")
            raise HTTPException(status_code=400, detail="Nome não pode ser vazio, preencha seu nome no campo Nome e tente novamente!")
        if user.email == "":
            logger.error("Erro ao criar usuário")
            raise HTTPException(status_code=400, detail="E-mail não pode ser vazio, digite seu e-mail no campo corretamente!")
        if user.password == "":
            logger.error("Erro ao criar usuário")
            raise HTTPException(status_code=400, detail="Senha senha não pode ser vazia, digite a senha criada no campo Senha e tente novamente!")

        hashed_pw = create_hash(user.password)
        db_user = User(name=user.name, email=user.email, password=hashed_pw, role="user")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Usuário criado com sucesso - Nome: {user.name}, E-mail: {user.email}")
        return db_user
    
    except SQLAlchemyError as e:
        logger.error(f"Erro na conexão com banco de dados ao criar usuário")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def get_user(db: Session, user_id: int, current_user: User):
    try:
        if current_user != "admin":
            logger.error(f"Operação negada: Usuário {current_user.id} tentou buscar dados de outro usuário")
            raise HTTPException(status_code=403, detail="Você não te permissão para acessar os dados de outro usuário")
        
        logger.info("Busca de usuário concluída com sucesso")
        return db.query(User).filter(User.id == user_id).first()
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def update_user(db: Session, user_id: int, user_data: UserUpdate, current_user: User):
    try:
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
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def delete_user(user_id: int, db: Session, current_user: User):
    try:
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
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def list_users(db: Session, current_user: User, skip: int = 0, limit: int = 10, name: str = None, email: str = None):
    try:
        if current_user.role != "admin":
            logger.error("Operação negada: um usuário tentou acessar dados de outro usuário")
            raise HTTPException(status_code=403, detail="Você não tem permissão para esse recurso")
        
        query = db.query(User)

        if name:
            query = query.filter(User.name.contains(name))
        if email:
            query = query.filter(User.email.contains(email))
        
        logger.info("Realizada consulta de usuários")
        return query.offset(skip).limit(limit).all()
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def get_user_by_email(db: Session, user_email: EmailStr) -> Optional[User]:
    try:
        return db.query(User).filter(User.email == user_email).first()
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")  


def patch_user(db: Session, user_id: int, user_patch: UserPatch, current_user: User):
    try:
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
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def activate_user(user_id: int, current_user: User, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
    
        if not user:
            logger.error("Usuário não encontrado durante ativação de usuário")
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
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
            
def deactivate_user(user_id: int, current_user: User, db: Session):
    try:
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
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")      

   
def promote_user_to_admin(user_id: int, current_user: User, db: Session):
    try:  
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
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

def get_data_current_user(current_user: User):
    if current_user is not None:
        logger.info("Consulta de dados do usuário logado realizada com sucesso")
        return current_user
    logger.error("Usuário não encontrado durante consulta de dados do usuário logado")
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

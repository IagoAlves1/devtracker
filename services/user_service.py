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

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        user.email = user_data.email

    if user_data.password is not None:
        from core.hashing import create_hash
        user.password = create_hash(user_data.password)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

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
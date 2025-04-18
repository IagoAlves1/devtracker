from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password
from schemas.user import UserUpdate
from core.hashing import create_hash
from typing import Optional
from pydantic import EmailStr

def create_user(db: Session, user: UserCreate):
    hashed_pw = create_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id, user_data: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        return None

    db_user.name = user_data.name
    db_user.email = user_data.email
    db_user.password = user_data.password

    db.commit()
    db.refresh(db_user)

    return db_user

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
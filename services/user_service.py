from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password

def create_user(db, name: str, email: str, password: str):
    hashed_pw = hash_password(user.password)
    user = User(name=name, email=email, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
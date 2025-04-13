from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import hash_password
from schemas.user import UserUpdate

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
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
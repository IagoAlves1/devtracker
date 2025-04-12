from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import create_user, get_user
from schemas.user import UserCreate, UserResponse
from core.database import Sessionlocal

router = APIRouter()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session =  Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
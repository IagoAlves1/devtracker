from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.database import Sessionlocal
from services.user_service import get_user_by_email
from core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return user
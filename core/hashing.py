from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password_plain: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plain, password_hash)


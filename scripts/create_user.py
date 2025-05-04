from core.database import SessionLocal
from services.user_service import create_user
from schemas.user import UserCreate

db = SessionLocal()

user_data = UserCreate(
    name="",
    email="",
    password=""
)

new_user = create_user(db=db, user=user_data)

print(f"Usuário criado com sucesso: {new_user.name}")
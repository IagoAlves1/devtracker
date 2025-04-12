from sqlalchemy.orm import Session
from core.database import Sessionlocal
from services.user_service import create_user

db = Sessionlocal()

new_user = create_user(db=db, name="Iago", email="iago@teste.com", password="senha123")

print(f"Usuário criado com sucesso: {new_user.name}")
from core.database import Sessionlocal
from services.user_service import update_user
from schemas.user import UserUpdate

db = Sessionlocal()

user_id = 1
user_data = UserUpdate(
    name = "",
    email = "",
    password = ""
)

user_atualizado = update_user(db=db, user_id=user_id, user_data=user_data)

if user_atualizado:
    print("Usuário atualizado com sucesso!")
    print(f"Nome: {user_atualizado.name}")
    print(f"Email: {user_atualizado.email}")
else:
    print("Usuário não encontrado.")
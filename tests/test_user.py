import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import Base
from services.user_service import create_user
from schemas.user import UserCreate

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")

def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user_data = UserCreate(
        name="Teste",
        email="teste@teste.com",
        password="123456"
    )

    user = create_user(db, user_data)

    assert user.id is not None
    assert user.name == "Teste"
    assert user.email == "teste@teste.com"

def test_update_other_user_forbidden(client):
    user_a = {
        "name": "Usuario A",
        "email": "usuario@example.com",
        "password": "senha123"
    }
    response = client.post("/users/", json=user_a)
    assert response.status_code == 201
    user_a_id = response.json()["id"]
    
    user_b = {
        "name": "Usuario B",
        "email": "usuariob@example.com",
        "password": "senha456"        
    }
    response = client.post("/users/", json=user_b)
    assert response.status_code == 201
    user_b_id = response.json()["id"]
    login_data = {
        "username": user_a["email"],
        "password": user_a["password"]
    }
    response = client.post("/login/", data=login_data)
    assert response.status_code == 200
    token_a = response.json()["access_token"]

    update_data = {
        "name": "Hackeado!"
    }
    headers = {"Authorization": f"Bearer {token_a}"}
    response = client.put(f"/user/{user_b_id}", json=update_data, headers=headers)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Você não tem permissão para atualizar este usuário."
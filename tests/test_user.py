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
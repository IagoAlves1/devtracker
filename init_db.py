from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.user import Base, User
import os
from core.database import create_tables
from core.hashing import create_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'crud_user.db')}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Banco de dados inicializado com sucesso!")

def create_master_admin(db: Session):
    existing_admin = db.query(User).filter(User.email == "admin@admin.com").first()
    if not existing_admin:
        admin_user = User(
            name="Admin Master",
            email="admin@admin.com",
            password=create_hash("admin123"),
            role="admin",
            is_active = True,
            is_deleted = False
        )
        db.add(admin_user)
        db.commit()
        print("Admin master criado com sucesso.") 
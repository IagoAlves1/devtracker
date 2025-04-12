from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base 
import os
from core.database import create_tables

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'devtracker.db')}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Banco de dados inicializado com sucesso!")
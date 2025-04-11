from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

from models.user import Base

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
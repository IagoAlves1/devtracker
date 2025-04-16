import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

env_path = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = "minha_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
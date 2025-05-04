import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

env_path = Path(__file__).parent.parent / '.env'

load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
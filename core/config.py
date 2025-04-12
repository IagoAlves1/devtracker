import os
from dotenv import load_dotenv
from pathlib import Path
from io import StringIO



env_path = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")


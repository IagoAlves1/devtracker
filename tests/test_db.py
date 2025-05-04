from core.database import SessionLocal

try:
    db = SessionLocal()
    print("Conexão com o banco de dados funcionando!")
finally:
    db.close()
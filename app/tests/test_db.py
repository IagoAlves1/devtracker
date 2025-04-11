from core.database import Sessionlocal

try:
    db = Sessionlocal()
    print("Conexão com o banco de dados funcionando!")
finally:
    db.close()
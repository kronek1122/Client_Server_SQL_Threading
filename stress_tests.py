from datetime import datetime
import os
from db import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

db_database = os.getenv('database')
db_user = os.getenv('user')
db_password = os.getenv('password')
db_host = os.getenv('host')
db_port = os.getenv('port')

def one_connection(i):
    start1= datetime.now()
    db = DatabaseManager(db_database, db_user, db_password, db_host)
    for x in range(i):
        db.get_users()
    stop1= datetime.now()
    return f'One db connection: {stop1-start1} seconds'

def many_connection(i):
    start2 = datetime.now()
    for x in range(i):
        db = DatabaseManager(db_database, db_user, db_password, db_host)
        db.get_users()
    stop2 = datetime.now()
    return f'Many db connection: {stop2-start2} seconds'

print(one_connection(1000))
print(many_connection(1000))
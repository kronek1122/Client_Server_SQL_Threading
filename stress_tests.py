import os
import threading
from db import DatabaseManager
from dotenv import load_dotenv

load_dotenv()
db_database = os.getenv('database')
db_user = os.getenv('user')
db_password = os.getenv('password')
db_host = os.getenv('host')
 

def stress_test():
    users = db.get_users()
    return users

if __name__ == "__main__":
    db = DatabaseManager(db_database, db_user, db_password, db_host)
    NUM_CONNECTIONS = 10000  # Number of concurrent connections

    threads = []
    for _ in range(NUM_CONNECTIONS):
        thread = threading.Thread(target=stress_test)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()



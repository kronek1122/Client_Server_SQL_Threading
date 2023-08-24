import os
import threading
import time
from db import DatabaseManager
from dotenv import load_dotenv

load_dotenv()
db_database = os.getenv('database')
db_user = os.getenv('user')
db_password = os.getenv('password')
db_host = os.getenv('host')


def stress_test(num_connections):
    def test():
        db = DatabaseManager(db_database, db_user, db_password, db_host)
        try:
            db.get_users()
            #time.sleep(1)
        except Exception as exp:
            print("Error get_users:", exp)

    threads = []
    for _ in range(num_connections):
        thread = threading.Thread(target=test)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    num_connections = 5000  # Number of concurrent connections

    stress_test(num_connections)

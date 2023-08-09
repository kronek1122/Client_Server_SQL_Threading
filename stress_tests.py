import os
import threading
from datetime import datetime
from db_connection_pool import ConnectionPool  
from db import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

db_database = os.getenv('database')
db_user = os.getenv('user')
db_password = os.getenv('password')
db_host = os.getenv('host')

def stress_test(pool, num_connections, num_iterations):
    def test():
        db = DatabaseManager(db_database, db_user, db_password, db_host)
        for _ in range(num_iterations):
            conn = pool.get_connection()
            try:
                users = db.get_users()
                print(users)
            except Exception as e:
                print("Error:", e)
            finally:
                pool.release_connection(conn)

    threads = []
    for _ in range(num_connections):
        thread = threading.Thread(target=test)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start= datetime.now()
    pool = ConnectionPool(5, 100)

    num_connections = 105  # Number of concurrent connections
    num_iterations = 100  # Number of times each connection will fetch users

    stress_test(pool, num_connections, num_iterations)
    stop = datetime.now()
    print (f'Time: {stop-start} seconds')
import os
import threading
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
                #print(users)

            except Exception as exp:
                print("Error:", exp)

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
    pool = ConnectionPool(5, 20)

    num_connections = 100  # Number of concurrent connections
    num_iterations = 1000  # Number of times each connection will fetch users

    stress_test(pool, num_connections, num_iterations)

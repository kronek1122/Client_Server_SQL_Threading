import psycopg2.pool
from dotenv import load_dotenv
import os

class ConnectionPool:
    def __init__(self):
        load_dotenv()
        self.min_connections = 5
        self.max_connections = 100
        self.host = os.getenv('host')
        self.port = os.getenv('port')
        self.database = os.getenv('database')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.pool = self.create_connection_pool()

    def create_connection_pool(self):
        return psycopg2.pool.SimpleConnectionPool(
            minconn=self.min_connections,
            maxconn=self.max_connections,
            host=self.host,
            port=self.port,
            dbname=self.database,
            user=self.user,
            password=self.password
        )
    
    def get_connection(self):
        return self.pool.getconn()

    def return_connection(self, conn):
        self.pool.putconn(conn)

    def close_all_connections(self):
        self.pool.closeall()
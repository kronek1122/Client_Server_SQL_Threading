import threading
from queue import Queue, Empty
from db import DatabaseManager
from dotenv import load_dotenv
import os

class ConnectionPool:
    def __init__(self, initial_connections=5, max_connections=100):
        load_dotenv()
        self.initial_connections = initial_connections
        self.max_connections = max_connections
        self.host = os.getenv('host')
        self.port = os.getenv('port')
        self.database = os.getenv('database')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.lock = threading.Lock()
        self.connections = Queue(maxsize=max_connections)
        self.initialize_connections()


    def initialize_connections(self):
        for i in range(self.initial_connections):
            connection = self.create_connection()
            if connection:
                self.connections.put(connection)


    def create_connection(self):
        connection = DatabaseManager(self.database, self.user, self.password, self.host)
        return connection
    

    def get_connection(self):
        try:
            connection = self.connections.get(timeout=2)
        except Empty:
            connection = self.create_connection
        return connection


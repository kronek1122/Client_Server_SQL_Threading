import threading
import time
import os
from queue import Queue, Empty, Full
from db import DatabaseManager
from dotenv import load_dotenv

class ConnectionPool:
    def __init__(self, min_connections=5, max_connections=100):
        load_dotenv()
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.host = os.getenv('host')
        self.port = os.getenv('port')
        self.database = os.getenv('database')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.lock = threading.Lock()
        self.connections = Queue(maxsize=max_connections)
        self.initialize_connections()

        self.connections_check = threading.Thread(target=self.connections_manager)
        self.connections_check.daemon = True
        self.connections_check.start()

    def initialize_connections(self):
        for _ in range(self.min_connections):
            connection = self.create_connection()
            if connection:
                self.connections.put(connection)


    def create_connection(self):
        try:
            connection = DatabaseManager(self.database, self.user, self.password, self.host)
            return connection
        except Exception as exp:
            print("Error creating connection:", exp)
            return None


    def get_connection(self):
        try:
            connection = self.connections.get(timeout=2)
        except Empty:
            try:
                self.initialize_connections()
                connection = self.connections.get(timeout=2)
            except Full:
                raise Exception('Connection pool limit reached')  
        return connection


    def connections_manager(self):
        while True:
            time.sleep(60)
            with self.lock:
                while self.connections.qsize()>self.min_connections:
                    connection = self.connections.get()
                    try:
                        connection.close()
                    except Exception:
                        pass


    def destroy_connections(self):
        with self.lock:
            while not self.connections.empty():
                connection = self.connections.get()
                try:
                    connection.close()
                except Exception:
                    pass
                    

    def release_connection(self, connection):
        try:
            self.connections.put(connection, timeout=2)
        except Full:
            try:
                connection.close()
            except Exception:
                pass


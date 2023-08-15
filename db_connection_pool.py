import threading
import time
import os
from queue import Queue, Empty, Full
from db import DatabaseManager
from dotenv import load_dotenv

class ConnectionPool:
    def __init__(self, min_connections=5, max_connections=50):
        load_dotenv()
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.host = os.getenv('host')
        self.port = os.getenv('port')
        self.database = os.getenv('database')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.semaphore = threading.Semaphore(max_connections)
        self.connections = Queue(maxsize=max_connections)
        self.start_time = time.time()
        self.connections_released = 0
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
        with self.semaphore:
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
            time.sleep(2)
            with self.semaphore:
                while self.connections.qsize()>self.min_connections:
                    connection = self.connections.get()
                    try:
                        connection.close()
                    except Exception:
                        pass

            print(f"""
                Time from start: {round(time.time() - self.start_time, 2)}
                Realised connections: {self.connections_released}
                Active connections: {self.connections.qsize()}
""")


    def destroy_connections(self):
        with self.semaphore:
            while not self.connections.empty():
                connection = self.connections.get()
                try:
                    connection.close()
                except Exception:
                    pass
                    

    def release_connection(self, connection):
        with self.semaphore:
            try:
                self.connections.put(connection, timeout=2)
            except Full:
                try:
                    connection.close()
                except Exception:
                    pass
            self.connections_released += 1

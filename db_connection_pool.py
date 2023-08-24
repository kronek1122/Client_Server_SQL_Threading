import threading
import time
import os
from queue import Queue, Empty, Full
import psycopg2
from dotenv import load_dotenv

class ConnectionPool:
    def __init__(self, database, user, password, host):
        load_dotenv()
        self.min_connections = 4
        self.max_connections = 50
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connections = Queue(maxsize=self.max_connections)
        self.semaphore = threading.Semaphore()
        self.start_time = time.time()
        self.connections_released = 0
        self.active_connections = 0
        self.initialize_connections()

        self.connections_check = threading.Thread(target=self.connections_manager)
        self.connections_check.daemon = True
        self.connections_check.start()

    def initialize_connections(self):
        for _ in range(self.min_connections):
            self.create_connection()


    def create_connection(self):
        try:
            connection = psycopg2.connect(self.database, self.user, self.password, self.host)
            self.connections.put(connection)
            return connection
        except Exception as exp:
            print("Error creating connection:", exp)
            return None


    def get_connection(self):
        with self.semaphore:
            try:
                connection = self.connections.get(timeout=2)
                self.active_connections +=1
            except Empty:
                if self.connections.qsize() + self.active_connections < self.max_connections:
                    self.create_connection()
                    connection = self.connections.get(timeout=2)
                    self.active_connections +=1
                else:
                    while True:
                        try:
                            connection = self.connections.get(timeout=2)
                            break
                        except Empty:
                            pass
            return connection


    def connections_manager(self):
        while True:
            while self.connections.qsize()>self.min_connections:
                connection = self.connections.get()
                try:
                    connection.close()
                except Exception as exp:
                    print("Error:", exp)

            print(f"""
                Time from start: {round(time.time() - self.start_time, 2)}
                Realised connections: {self.connections_released}
                Active connections: {self.active_connections}
                Connections in Queue: {self.connections.qsize()}
                """)
            time.sleep(3)


    def destroy_connections(self):
        with self.semaphore:
            while not self.connections.empty():
                connection = self.connections.get()
                try:
                    connection.close()
                except Exception as exp:
                    print("Error:", exp)


    def release_connection(self, connection):
        with self.semaphore:
            try:
                self.connections.put(connection, timeout=2)
                self.active_connections -=1
            except Full:
                try:
                    connection.close()
                except Exception as exp:
                    print("Error:", exp)
            self.connections_released += 1


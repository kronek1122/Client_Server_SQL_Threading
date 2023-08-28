import psycopg2
from db_connection_pool import ConnectionPool
import time

class DatabaseManager:
    def __init__(self, database, user, password, host):
        self.connection_pool = ConnectionPool(database, user, password, host)

    def add_user(self, user_name, password, is_admin):
        query = "INSERT INTO user_info (user_name, password, is_admin) VALUES (%s, %s, %s);"
        user_table = f"""CREATE TABLE {user_name} (
                        message_id SERIAL PRIMARY KEY,
                        message_text VARCHAR(255),
                        sender VARCHAR(50),
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_unread BOOLEAN);"""
        try: 
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query, (user_name, password, is_admin))
            curr.execute(user_table)
            conn.commit()
            msg = 'User succesfully registered'
            self.connection_pool.release_connection(conn)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            msg = 'User already exist'
        return msg


    def login_user(self, user_name, password):
        query = "SELECT * FROM user_info WHERE user_name = (%s) AND password = (%s)"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query, (user_name, password))
        rows = curr.fetchall()
        self.connection_pool.release_connection(conn)

        if len(rows)>0:
            msg = "User succesfully login"
        else:
            msg = "Wrong password or user doesn't exist"
            user_name = ''
        return msg, user_name


    def get_users(self):
        query = "SELECT user_name FROM user_info"
        try:
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            result = curr.fetchall()
            time.sleep(0.1) #Added only to slow down working of threading
            self.connection_pool.release_connection(conn)
            return result
        except psycopg2.errors.ProgrammingError as exp:
            return f"Error getting users: {exp}"
    

    def get_user(self,user_name):
        query = f"SELECT user_name FROM user_info WHERE user_name = '{user_name}'"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result =  curr.fetchone()
        self.connection_pool.release_connection(conn)
        return result


    def send_message(self, user_name, message, sender):
        values = (' '.join(message), sender, True)
        query = f"INSERT INTO {user_name} (message_text, sender, is_unread) VALUES {values};"
        try: 
            conn = self.connection_pool.get_connection()
            curr = conn.cursor()
            curr.execute(query)
            conn.commit()
            msg = f'You successfully send message to user {user_name}'
            self.connection_pool.release_connection(conn)
        except psycopg2.errors.UndefinedTable:
            conn.rollback()
            msg = "User doesn't exist"
        return msg


    def count_unread(self, user_name):
        query = f"SELECT COUNT(*) FROM {user_name} WHERE is_unread = 'TRUE';"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchone()
        self.connection_pool.release_connection(conn)
        if result is not None:
            return result[0]
        else:
            return 0


    def is_user_admin(self, user_name):
        query = f"SELECT is_admin FROM user_info WHERE user_name = '{user_name}'"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchone()
        self.connection_pool.release_connection(conn)
        if result is not None:
            is_admin = bool(result[0])
            return is_admin
        else:
            return False
        

    def get_message(self, user_name):
        query = f"SELECT sender, TO_CHAR(timestamp, 'YYYY-MM-DD HH:MI:SS'), message_text FROM {user_name};"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchall()
        self.connection_pool.release_connection(conn)
        if result == []:
            result = "Inbox is empty"
        return result
    

    def get_unread_message(self, user_name):
        query = f"SELECT sender, TO_CHAR(timestamp, 'YYYY-MM-DD HH:MI:SS'), message_text FROM {user_name} WHERE is_unread = TRUE;"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchall()
        self.connection_pool.release_connection(conn)
        return result


    def is_msg_unread(self, user_name):
        query = f"SELECT is_unread FROM {user_name} WHERE is_unread = TRUE;"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        result = curr.fetchone()
        self.connection_pool.release_connection(conn)
        if result is not None:
            is_unread = bool(result[0])
            return is_unread
        else:
            return False
        

    def change_from_unread(self,user_name):
        query = f"UPDATE {user_name} SET is_unread = FALSE WHERE is_unread = TRUE;"
        conn = self.connection_pool.get_connection()
        curr = conn.cursor()
        curr.execute(query)
        conn.commit()
        self.connection_pool.release_connection(conn)



import socket as s
import json
from datetime import datetime
from user import User

class Server:

    def __init__(self, host, port, info):
        self.host = host
        self.port = port
        self.info = info
        self.start_time = datetime.now()
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(100)
        self.user = User()


    def available_commands(self):
        '''Return json file with list of available commands'''
        msg = {
            'uptime': "returns the lifetime of the server",
            'info': "returns the version of the server, the date of its creation",
            'help': "returns a list of available commands",
            'stop': "stops server and client",
            'register <user name> <password>' : 'create new user',
            'login <user name> <password>' : 'log in user',
            'users' : 'return all user list',
            'send <user name> <massage>': 'send a message to the selected user',
            'inbox' : 'check messages in your inbox',
            'unread' : 'check only unread messages',
            'disconnect' : 'disconnect client from server'
        }
        return json.dumps(msg, indent=1)


    def uptime(self):
        '''Return json file with lifetime of the server'''
        return json.dumps(str(datetime.now() - self.start_time))


    def json_unpacking(self, data):
        '''Unpacking jsonfile'''
        unpacking_data = []
        unpacking_data = data.split(' ')
        return unpacking_data


    def start(self):
        '''Starting the server'''

        connection, address = self.server_socket.accept()

        print(f'Connected by {address}')
        while True:
            query = connection.recv(1024).decode('utf8')

            if not query:
                break

            query_list = self.json_unpacking(query)

            if query_list[0] == 'uptime':
                connection.send(self.uptime().encode('utf8'))

            elif query_list[0] == 'info':
                connection.send(self.info.encode('utf8'))

            elif query_list[0] == 'help':
                connection.send(self.available_commands().encode('utf8'))

            elif query_list[0] == 'register':
                try:
                    connection.send(self.user.register(query_list[1],query_list[2],query_list[3]).encode('utf8'))
                except:
                    connection.send(self.user.register(query_list[1],query_list[2]).encode('utf8'))

            elif query_list[0] == 'login':
                connection.send(self.user.login(query_list[1],query_list[2]).encode('utf8'))

            elif query_list[0] == 'users':
                connection.send(self.user.users_list().encode('utf8'))

            elif query_list[0] == 'send':
                connection.send(self.user.send_message(query_list[1],query_list[2:]).encode('utf8'))

            elif query_list[0] == 'inbox':
                connection.send(self.user.check_inbox(query_list).encode('utf8'))

            elif query_list[0] == 'unread':
                connection.send(self.user.check_unread_messages().encode('utf8'))

            elif query_list[0] == 'stop':
                connection.send(('server closed').encode('utf8'))
                self.server_socket.close()
                break

            else:
                connection.send(('Unknown command').encode('utf8'))

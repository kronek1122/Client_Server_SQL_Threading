from server import Server

HOST = '127.0.0.1'
PORT = 65432
INFO = 'version: 0.3.3; creation date: 12.03.2023r'
server = Server(HOST,PORT,INFO)

server.start()
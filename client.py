'''Client socket API'''

import socket as s

class ClientSocket:
    HOST = '127.0.0.1'
    PORT = 65432
    
    def __init__(self):
        self.client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

    def send_receive(self):
        while True:
            user_command = input('Enter the command! (Type help for command list):  ').encode('utf8')
            self.client_socket.sendall(user_command)
            data = self.client_socket.recv(1024).decode('utf8')
            if data == 'server closed':
                print(data)
                break
            else:
                print(data)
                
if __name__ == '__main__':
    client = ClientSocket()
    client.send_receive()

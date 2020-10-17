import socket
import sys


class Client:
    def __init__(self, bind_ip='localhost', bind_port=80):
        self.bind_ip = bind_ip
        self.bind_port = bind_port

        # Conectando o Socket TCP/IP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.bind_ip, self.bind_port))

    def run(self):
        message = "DELE arquivo"

        while True:
            self.server.sendall(message.encode('ascii'))

            data = self.server.recv(1024)
            print('Received from the server :', str(data.decode('ascii')))

            ans = input('\nDo you want to continue(y/n) :')
            if ans == 'y':
                continue
            else:
                break

        self.server.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    client = Client(HOST, PORT)
    client.run()

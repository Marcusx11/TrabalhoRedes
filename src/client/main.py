import socket
import sys


class Client:
    def __init__(self, bind_ip='localhost', bind_port=80):
        self.bind_ip = bind_ip
        self.bind_port = bind_port

    def __connect_socket(self):
        # Tentando  conectar com o servidor TCP/IP
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((self.bind_ip, self.bind_port))
        except:
            print('Não foi possivel realizar conexão com {}:{}'.format(
                self.bind_ip, self.bind_port))
            quit()

    def __desconnect_socket(self):
        print("A conexão com {}:{} foi encerrada".format(
            self.bind_ip, self.bind_port))
        self.server.close()
        quit()

    def run(self):
        self.__connect_socket()

        while True:
            try:
                cmd = input('> ')
                cmd_splited = cmd.split(' ')[0].upper()

                self.server.sendall(cmd.encode())
                if cmd_splited == 'QUIT':
                    self.__desconnect_socket()

                data = self.server.recv(1024)

                if data:
                    print(str(data.decode('utf-8')))

            except KeyboardInterrupt:
                self.__desconnect_socket()

        self.server.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    client = Client(HOST, PORT)
    client.run()

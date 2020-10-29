import socket
import sys
import time

BUFFER_SIZE = 4096


class Client:
    def __init__(self, host_name='localhost', bind_port=80):
        self.bind_ip = socket.gethostbyname(host_name)
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

    def __receive_data(self):

        # file_size = int.from_bytes(self.server.recv(BUFFER_SIZE), "big")

        # print(file_size)

        # Tentando abrir o arquivo
        file_name = input("Digite o nome e a extensão do arquivo a ser recebido: ").strip()
        file = None

        # Tentando pegar os dados
        try:
            file = open(file_name, "wb")
            # Pegando-se os dados
            while True:
                data = self.server.recv(BUFFER_SIZE)
                if not data:
                    break

                file.write(data)

        except Exception as e:
            self.server.sendall(b'Nao foi possivel criar o arquivo')

        finally:
            file.close()

    def run(self):
        self.__connect_socket()

        while True:
            try:
                cmd = input('> ')
                cmd_splited = cmd.split(' ')[0]

                self.server.sendall(cmd.encode())
                if cmd_splited == 'QUIT':
                    self.__desconnect_socket()

                self.__receive_data()

            except KeyboardInterrupt:
                self.__desconnect_socket()

        self.server.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    client = Client(HOST, PORT)
    client.run()

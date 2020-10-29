import socket
import sys
import time

BUFFER_SIZE = 4096


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

    def __receive_data(self, timeout=2):
        self.server.setblocking(True)
        total_data = []

        # Começando o tempo
        begin_time = time.time()

        # Pegando-se os dados
        while True:
            # Sai do loop após o timeout e com dados
            if total_data and time.time() - begin_time > timeout:
                break

            # Sai do loop após esperar o dobro do timeout, sem dados
            elif time.time() - begin_time > timeout * 2:
                break

            # Recebendo os dados
            try:
                data = self.server.recv(BUFFER_SIZE)
                if data:
                    total_data.append(data)
                    begin_time = time.time()
                else:
                    # Sleep indicando um intervalo
                    time.sleep(0.1)

            except:
                pass

        # Retornando o vetor de bytes
        return b''.join(total_data)

    def run(self):
        self.__connect_socket()

        while True:
            try:
                cmd = input('> ')
                cmd_splited = cmd.split(' ')[0]

                self.server.sendall(cmd.encode())
                if cmd_splited == 'QUIT':
                    self.__desconnect_socket()

                final_data = self.__receive_data()

                if final_data:
                    file_name = input("Digite o nome e a extensão do arquivo a ser recebido: ").strip()
                    file = open(file_name, "wb")
                    file.write(final_data)

                    # print(str(data.decode()))
                    print("oba!")

                    file.close()

            except KeyboardInterrupt:
                self.__desconnect_socket()

        self.server.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    client = Client(HOST, PORT)
    client.run()

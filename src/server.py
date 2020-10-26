import socket
import sys
from FTP import FTPThread
import threading


class Server:
    def __init__(self, bind_ip='localhost', bind_port=80):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.thread_cont = 0

    def __create_socket(self):
        try:
            # Criando o Socket TCP/IP
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # A opção SO_REUSEADDR é utilizada para garantir que a proxima
            # conexão utilize o mesmo socket caso o mesmo estiver aberto
            # Para mais informações consultar o card Links e refencia no Trello
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.bind_ip, self.bind_port))

            # Faz o servidor atender até 5 conexões simultaneas
            self.server.listen(5)

            print("Servidor escutando na porta: {} e IP {}".format(
                self.bind_port, self.bind_ip))
        except OSError:
            print('O endereço {}:{} já esta sendo utilizado.'.format(
                self.bind_port, self.bind_ip))
            quit()

    def run(self):
        """
        Método que vai fazer o servidor executar e esperar por requisições
        """
        self.__create_socket()
        client = None

        while True:
            try:  # Tenta aceitar a coenxão de um cliente

                # Espera por alguma conexão do cliente e tenta aceitá-la
                client, addr = self.server.accept()

                if not client:
                    break

                print("\nCliente conectado! Seu endereço: {}:{}".format(
                    addr[0], addr[1]))

                ftp = FTPThread(client)

                # Thread daemon é encerrada junto com a thread principal
                ftp.daemon = True
                ftp.run()

            except KeyboardInterrupt:
                self.server.close()
                quit()

            # TODO fazer uma mensagem de erro mais formalizada para cada caso de erro
            # except EOFError or FileNotFoundError or IOError or ConnectionError:
            except Exception as e:
                print("SERVER.PY > Ocorreu algum erro na requisição do cliente...")
                print(str(e))
                client.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    tcp_server = Server(HOST, PORT)
    tcp_server.run()

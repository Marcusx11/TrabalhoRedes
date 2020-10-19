import socket
import sys
from FTP import FTPThread


class Server:
    def __init__(self, bind_ip='localhost', bind_port=80):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.thread_cont = 0

        # Criando o Socket TCP/IP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.bind_ip, self.bind_port))

        # Faz o servidor atender até 5 conexões simultaneas
        self.server.listen(5)

        print("> Servidor escutando na porta: {} e IP {}".format(
            self.bind_port, self.bind_ip))

    def run(self):
        """
        Método que vai fazer o servidor executar e esperar por requisições
        """
        print("Servidor esperando por conexão...\n")

        is_running = True

        client = None

        while is_running:
            try:  # Tenta aceitar a coenxão de um cliente

                # Espera por alguma conexão do cliente e tenta aceitá-la
                client, addr = self.server.accept()

                print("Cliente conectado! Seu endereço: {}:{}".format(
                    addr[0], addr[1]))

                ftp = FTPThread(client)
                ftp.run()

            except KeyboardInterrupt:
                client.close()
                sys.exit()

            # TODO fazer uma mensagem de erro mais formalizada para cada caso de erro
            # except EOFError or FileNotFoundError or IOError or ConnectionError:
            except:
                print("SERVER.PY > Ocorreu algum erro na requisição do cliente...")
                client.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    tcp_server = Server(HOST, PORT)
    tcp_server.run()

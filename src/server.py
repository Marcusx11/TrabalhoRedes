import socket
import threading
import sys

print_lock = threading.Lock()


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

    def handle_client(self,  client):
        """
        Trata cada caso de cliente que esteja requisitando algo para o servidor
        """
        while True:
            data = client.recv(1024)

            if not data:
                print('Bye')
                print_lock.release()
                break

            print("Thread nº: " + str(self.thread_cont))

            # Retorna a string invertida
            data = data[::-1]

            client.sendall(data)
            self.thread_cont = self.thread_cont + 1

        # Fechando coenxão após o tratamento de sua requisição
        client.close()

    # Método que vai fazer o servidor executar e esperar por requisições
    def run(self):
        print("Servidor esperando por conexão...\n")

        is_running = True
        while is_running:

            # Tenta aceitar a coenxão de um cliente
            try:

                # Espera por alguma conexão do cliente e tenta aceitá-la
                client, addr = self.server.accept()

                print("Cliente conectado! Seu endereço: {}:{}".format(
                    addr[0], addr[1]))

                # Criando uma thread para tratar o novo cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, ))

                client_thread.start()

            except KeyboardInterrupt:
                sys.exit()
                client_thread._stop()

            # TODO fazer uma mensagem de erro mais formalizada para cada caso de erro
            # except EOFError or FileNotFoundError or IOError or ConnectionError:
            except:
                print("Ocorreu algum erro na requisição do cliente...")
                client.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    tcp_server = Server(HOST, PORT)
    tcp_server.run()

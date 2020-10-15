import socket
import threading


# Criando a classe do servidor TCP
class TCPServer:
    def __init__(self, bind_ip='localhost', bind_port=80):
        self.bind_ip = bind_ip
        self.bind_port = bind_port

        # Criando o Socket TCP/IP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.bind_ip, self.bind_port))

        # Inicializando variáveis locais da conexão do cliente
        self.client = None
        self.cli_address = None

        print("-- Servidor escutando na porta: " + str(self.bind_port) + " e IP: " + str(self.bind_ip) + "\n")

    # Método para tratar cada caso de cliente que esteja requisitando algo para o servidor
    def handle_client(self):
        request = self.client.recv(1024)

        # Enviando uma mensagem para o cliente
        self.client.send("Olár!")
        self.client.close()  # Fechando coenxão após o tratamento de sua requisição

    # Método que vai fazer o servidor executar e esperar por requisições
    def run_server(self):
        # Faz o servidor atender até 5 conexões simultaneas
        self.server.listen(5)

        is_running = True

        while is_running:
            print("Servidor esperando por conexão...\n")

            try:  # Tenta aceitar a coenxão de um cliente

                # Espera por alguma conexão do cliente e tenta aceitá-la
                self.client, self.cli_address = self.server.accept()

                print("Cliente conectado! Seu endereço: " + str(self.cli_address[0]) + str(self.cli_address[1]))

                # Criando uma thread para tratar o novo cliente
                client_thread = threading.Thread(target=self.handle_client, args=(self.client,))
                client_thread.start()

            # TODO fazer uma mensagem de erro mais formalizada para cada caso de erro
            except EOFError or FileNotFoundError or IOError or ConnectionError:
                print("Ocorreu algum erro na requisição do cliente...")


if __name__ == "__main__":
    tcp_server = TCPServer()
    tcp_server.run_server()

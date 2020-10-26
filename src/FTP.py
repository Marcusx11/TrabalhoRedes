from threading import Thread
import sys
import socket


class FTPThread(Thread):
    def __init__(self, client: socket.socket, client_ip, client_port):
        super().__init__()
        self.client = client
        self.client_ip = client_ip
        self.client_port = client_port
        self.thread = None

        self.COMMANDS = {
            'RETR': self.__RETR,
            'STOP': self.__STOR,
            'DELE': self.__DELE,
            'MKD': self.__MKD,
            'NLST': self.__NLST,
            'LIST': self.__LIST,
            'QUIT': self.__QUIT,
            'HELP': self.__HELP,
        }

    def __RETR(self, cmd: list):
        """Obtém uma cópia do arquivo especificado (download para o cliente)."""
        print('RETR')
        self.client.sendall(b'RETR')

    def __STOR(self, cmd: list):
        """Envia uma cópia do arquivo especificado (upload para o servidor)."""
        print('STOR')
        self.client.sendall(b'STOP')

    def __DELE(self, cmd: list):
        """Apaga um arquivo"""
        print('DELE')
        self.client.sendall(b'DELE')

    def __MKD(self, cmd: list):
        """Cria um diretório."""
        print('MKD')
        self.client.sendall(b'MKD')

    def __NLST(self, cmd: list):
        """Lista os nomes dos arquivos de um diretório."""
        print('NLST')
        self.client.sendall(b'NLIST')

    def __LIST(self, cmd: list):
        """
        Retorna informações* do arquivo ou diretório especificado 
        (* ex.: nome, tamanho, data de modificação, etc)
        """
        print('LIST')
        self.client.sendall(b'LIST')

    def __QUIT(self, cmd: list):
        """Desconecta"""
        try:
            self.client.sendall(b'Encerrando conexao com o servidor')
        finally:
            print('Fechando a conexão com o cliente {}:{}'.format(
                self.client_ip, self.client_port))
            self.client.close()
            quit()

    def __HELP(self, cmd: list):
        """
        Retorna documentação de uso (de um comando específico, se 
        especificado; ou então um documento geral de ajuda).
        """
        print('HELP')
        self.client.sendall(b'HELP')

    def run(self):
        while True:
            try:
                request = self.client.recv(1024)
                cmd = request.decode('utf-8').split(" ")

                if cmd[0] not in self.COMMANDS:
                    err = '{} não é um comando valido.'.format(cmd[0])
                    self.client.sendall(err.encode('utf-8'))
                    break

                cmd[0] = cmd[0].upper()
                self.COMMANDS[cmd[0]](cmd)

            except Exception as e:
                print("Ocorreu algum erro na requisição do cliente...")
                print(str(e))
                break
                # self.thread.join()
        self.client.close()

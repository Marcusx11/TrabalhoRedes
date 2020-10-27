import threading
import sys
import shutil
from pathlib import Path
import socket

print_lock = threading.Lock()


class FTPThread:
    def __init__(self, client: socket.socket):
        self.client = client
        self.path = 'src/server/files/'

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
        try:
            Path(self.path + cmd[1]).mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            msg = 'O caminho "{}" já existe.'.format(cmd[1])
            print(FileExistsError)
            self.client.sendall(msg.encode())

        msg = '"{}" foi criado com sucesso!'.format(cmd[1])
        self.client.sendall(msg.encode())

    def __RMD(self, cmd: list):
        try:
            shutil.rmtree(self.path + cmd[1])

        except FileNotFoundError:
            msg = '"{}" não foi encontrado'.format(cmd[1])
            self.client.sendall(msg.encode())

        msg = '"{}" foi excluido com sucesso!'.format(cmd[1])
        self.client.sendall(msg.encode())

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
        print('QUIT')
        self.client.sendall(b'QUIT')

    def __HELP(self, cmd: list):
        """
        Retorna documentação de uso (de um comando específico, se 
        especificado; ou então um documento geral de ajuda).
        """
        print('HELP')
        self.client.sendall(b'HELP')

    def __select_command(self, request: str):
        request = request.strip().split(" ")

        COMMANDS = {
            'RETR': self.__RETR,
            'STOP': self.__STOR,
            'DELE': self.__DELE,
            'MKD': self.__MKD,
            'RMD': self.__RMD,
            'NLST': self.__NLST,
            'LIST': self.__LIST,
            'QUIT': self.__QUIT,
            'HELP': self.__HELP,
        }

        # CMD <option>
        COMMANDS[request[0].upper()](request)

    def run(self):

        client_thread = None

        while True:
            try:
                request = self.client.recv(1024)

                print("Comando: ", request)

                if not request:
                    print('Bye')
                    print_lock.release()
                    break

                client_thread = threading.Thread(
                    target=self.__select_command, args=(request.decode('ascii'),))
                client_thread.start()

            except:
                print("FTP > Ocorreu algum erro na requisição do cliente...")
                client_thread._stop()
                break

        self.client.close()

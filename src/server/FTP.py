from threading import Thread
import sys
import os
import shutil
from pathlib import Path
import socket


class FTPThread(Thread):
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        self.cwd = os.getcwd() + '/src/server/storage/'  # current working directory

        self.COMMANDS = {
            'RETR': self.__RETR,
            'STOP': self.__STOR,
            'DELE': self.__DELE,
            'MKD': self.__MKD,
            'MKDIR': self.__MKD,
            'RMD': self.__RMD,
            'NLST': self.__NLST,
            'LIST': self.__LIST,
            'QUIT': self.__QUIT,
            'EXIT': self.__QUIT,
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

    def __MKD(self, cmd: str):
        """Cria um diretório."""

        path = cmd.split(" ")[1]
        dirname = os.path.join(self.cwd, path)

        try:
            if not path:
                self.client.sendall(b'Argumento faltando <dirname>')
            else:
                Path(dirname).mkdir(parents=True, exist_ok=False)

        except FileExistsError:
            msg = 'O diretório "{}" já existe.'.format(path)
            self.client.sendall(msg.encode())
            pass

        finally:
            msg = '"{}" foi criado com sucesso!'.format(path)
            self.client.sendall(msg.encode())

    def __RMD(self, cmd: str):
        """Delete um diretório junto com todos os seus arquivos"""

        path = cmd.split(" ")[1]
        dirname = os.path.join(self.cwd, path)

        try:
            if not path:
                self.client.sendall(b'Argumento faltando <dirname>')
            else:
                shutil.rmtree(dirname)

        except FileNotFoundError:
            msg = '"{}" não foi encontrado'.format(path)
            self.client.sendall(msg.encode())
            pass

        finally:
            msg = '"{}" foi excluido com sucesso!'.format(path)
            self.client.sendall(msg.encode())

    def __NLST(self, cmd: str):
        """Lista os nomes dos arquivos de um diretório."""
        path = ''
        if cmd.split(" ") == 2:
            path = cmd.split(" ")[1]

        dirname = os.path.join(self.cwd, path)

        items = os.listdir(dirname)

        if items:
            dir_list = "\n".join(items)
            self.client.sendall(dir_list.encode())
        else:
            self.client.sendall('Diretório vazio'.encode('utf-8'))

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
        COMMANDS = {
            'RETR': self.__RETR,
            'STOP': self.__STOR,
            'DELE': self.__DELE,
            'MKD': self.__MKD,
            'MKDIR': self.__MKD,
            'RMD': self.__RMD,
            'NLST': self.__NLST,
            'LIST': self.__LIST,
            'QUIT': self.__QUIT,
            'EXIT': self.__QUIT,
            'HELP': self.__HELP,
        }

        # CMD <option>
        cmd = request.split()[0].upper()
        COMMANDS[cmd](request)

    def run(self):
        while True:
            try:
                request = self.client.recv(1024)
                if not request:
                    print('bye')
                    break

                request_decoded = request.decode()

                print("Comando: ", request)

                cmd = request_decoded.split(" ")[0].upper()
                print("Comando: ", cmd)

                if cmd not in self.COMMANDS:
                    err = '{} não é um comando valido.'.format(cmd)
                    self.client.sendall(err.encode())
                    continue

                self.COMMANDS[cmd](request_decoded)

            except Exception as e:
                print("FTP > Ocorreu algum erro na requisição do cliente...")
                print(str(e))
                break

        # self.client.close()

from threading import Thread
import sys
import os
import shutil
import subprocess
from pathlib import Path
import socket

BUFFER_SIZE = 1024


class FTPThread(Thread):
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        # current working directory
        self.cwd = os.path.join(os.getcwd(), "storage")

        self.COMMANDS = {
            'RETR': self.__RETR,
            'GET': self.__RETR,
            'STOR': self.__STOR,
            'PUT': self.__STOR,
            'DELE': self.__DELE,
            'RM': self.__DELE,
            'MKD': self.__MKD,
            'MKDIR': self.__MKD,
            'RMD': self.__RMD,
            'NLST': self.__NLST,
            'LS': self.__NLST,
            'LIST': self.__LIST,
            'LSL': self.__LIST,
            'QUIT': self.__QUIT,
            'EXIT': self.__QUIT,
            'HELP': self.__HELP,
            '?': self.__HELP,
        }

    def __RETR(self, cmd: str):
        """Obtém uma cópia do arquivo especificado (download para o cliente)."""
        # Pegando-se caminho do arquivo
        try:
            path = cmd.strip().split(" ")[1]
            if not path:
                self.client.sendall(b'Argumento faltando <pathname>')
                return

            dir_name = os.path.join(self.cwd, path)
            if not os.path.isfile(dir_name):
                self.client.sendall(b'error Arquivo nao encontrado')
                return

            file_size = os.path.getsize(dir_name)
            self.client.sendall(f'ok {file_size}'.encode())

            request = self.client.recv(BUFFER_SIZE).decode()
            if request == 'ok':
                with open(dir_name, 'rb') as file:
                    data = file.read(BUFFER_SIZE)
                    while data:
                        self.client.sendall(data)
                        data = file.read(BUFFER_SIZE)

                self.client.sendall(b'ok')
        except FileNotFoundError:
            print('arquivo n existe')
            self.client.sendall(b'Arquivo nao encontrado')
        except Exception as e:
            self.client.sendall(str(e).encode())

    def __STOR(self, cmd: list):
        """Envia uma cópia do arquivo especificado (upload para o servidor)."""
        parts = cmd.strip().split(" ")

        if not parts[1]:
            self.client.sendall(b'Argumento faltando <pathname>')
            return

        if not parts[2]:
            self.client.sendall(b'Argumento faltando <filesize>')
            return

        path = parts[1]
        dir_name = os.path.join(self.cwd, path)
        file_size = int(parts[2])

        self.client.sendall(b'ok')

        try:
            file = open(dir_name, 'wb')
            download_size = 0
            while download_size < file_size:
                data = self.client.recv(BUFFER_SIZE)
                download_size += len(data)
                file.write(data)
            file.close()

            print('{} foi upado com sucesso!'.format({path}))
        except Exception as e:
            print('e', str(e))

    def __DELE(self, cmd: list):
        """Apaga um arquivo"""
        parts = cmd.strip().split(" ")

        if not parts[1]:
            self.client.sendall(b'Argumento faltando <filename>')
            return

        dir_name = os.path.join(self.cwd, parts[1])
        if not os.path.isfile(dir_name):
            self.client.sendall(b'error Arquivo nao encontrado')
            return

        os.remove(dir_name)

        self.client.sendall(b'Arquivo removido com sucesso!')

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
        if len(cmd.split(" ")) == 2:
            path = cmd.split(" ")[1]

        dirname = os.path.join(self.cwd, path)

        items = os.listdir(dirname)

        if items:
            dir_list = "\n".join(items)
            self.client.sendall(dir_list.encode())
        else:
            self.client.sendall('Diretório vazio'.encode('utf-8'))

    def __LIST(self, cmd: str):
        """
        Retorna informações* do arquivo ou diretório especificado
        (* ex.: nome, tamanho, data de modificação, etc)
        """

        path = ''
        if len(cmd.split(" ")) == 2:
            path = cmd.split(" ")[1]

        path_file = os.path.join(self.cwd, path)

        if not os.path.exists(path_file):
            return self.client.sendall('error diretorio não encontrado ')

        response = subprocess.getstatusoutput(f'ls -l {path_file}')

        self.client.sendall(response[1].encode())

    def __QUIT(self, cmd: str):
        """Desconecta"""
        print('QUIT')
        self.client.sendall(b'QUIT')

    def __HELP(self, cmd: str):
        """
        Retorna documentação de uso (de um comando específico, se
        especificado; ou então um documento geral de ajuda).
        """

        HELP = {
            'RETR': 'RETR <pathname> -- Obtém uma cópia do arquivo especificado',
            'get': 'get -- Mesmo que RETR, apelido alternativo para o comando.',
            'STOR': 'STOR <pathname -- Envia uma cópia do arquivo especificado (upload para o servidor).',
            'put': 'put -- Mesmo que STOR, apelido alternativo para o comando.',
            'DELE': 'DELE <pathname> -- Apaga um arquivo do servidor.',
            'rm': 'rm -- Mesmo que DELE, apelido alternativo para o comando.',
            'MKD': 'MKD <dirname> -- Cria um novo diretório.',
            'mkdir': 'mkdir == Mesmo que MKD, apelido alternativo para o comando.',
            'NLST': 'NLST <pathname> -- Lista os nomes dos arquivos de um diretório.',
            'ls': 'ls -- Mesmo que NLST, apelido alternativo para o comando.',
            'LIST': 'LIST <pathname> -- Retorna informações do arquivo ou diretório especificado.',
            'QUIT': 'QUIT -- Encerra a conexão com o servidor.',
            'exit': 'exit -- Mesmo que QUIT, apelido alternativo para o comando.',
            'HELP': 'HELP <comando> -- Retorna documentação de uso (de um comando específico, se especificado; ou então um documento geral de ajuda).',
            '?': '? -- O mesmo que HELP, apelido alternativo para o comando.',
        }

        command = None
        if len(cmd.split(" ")) == 2:
            command = cmd.split(" ")[1]

        if command and command in HELP:
            self.client.sendall(HELP[command].encode())
        elif command and command not in HELP:
            msg = '{} não é um comando válido.'.format(command)
            self.client.sendall(msg.encode())
        else:
            all_help = "\n\n".join(HELP.values())
            self.client.sendall(all_help.encode())

    def run(self):
        while True:
            try:
                request = self.client.recv(1024)
                if not request:
                    print('bye')
                    break

                request_decoded = request.decode()

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

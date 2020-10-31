import socket
import sys
import os

BUFFER_SIZE = 1024


class Client:
    def __init__(self, bind_ip='localhost', bind_port=80):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.cwd = os.getcwd() + '/src/client/storage/'  # current working directory

        self.COMMANDS = {
            'RETR': self.__RETR,
            'GET': self.__RETR,
        }

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

    def __RETR(self, cmd: str):
        cmd_striped = cmd.strip().split(" ")

        if len(cmd_striped) < 2:
            print('Argumento faltando <pathname>')
            return

        path = cmd_striped[1]
        dir_name = os.path.join(self.cwd, path)

        if os.path.exists(dir_name):
            print('O arquivo {} já foi baixado anteriormente.'.format(path))
            return

        self.server.sendall(cmd.encode())

        response = self.server.recv(BUFFER_SIZE).decode().split(' ')
        
        if response[0] == 'error':
            print(response[1])
            return
        else:
            file_size = int(response[1])
        
        self.server.sendall(b'ok')

        try:
            file = open(dir_name, 'wb')
            download_size = 0
            while download_size < file_size:
                data = self.server.recv(BUFFER_SIZE)
                download_size += len(data)
                file.write(data)
            file.close()

            print('{} foi baixado com sucesso!'.format({path}))
        except Exception as e:
            print('e', str(e))

    def __STOR(self, cmd: str):
        try:
            path = cmd.strip().split(" ")[1]
            if not path:
                print('Argumento faltando <pathname>')
                return

            dir_name = os.path.join(self.cwd, path)
            if not os.path.isfile(dir_name):
                print('Arquivo nao encontrado')
                return

            file_size = os.path.getsize(dir_name)
            self.server.sendall((f'STOR {path} {file_size}').encode())
            
            response = self.server.recv(BUFFER_SIZE).decode()

            if response == 'ok':
                with open(dir_name, 'rb') as file:
                    data = file.read(BUFFER_SIZE)
                    while data:
                        self.server.sendall(data)
                        data = file.read(BUFFER_SIZE)

        except FileNotFoundError:
            print('Arquivo nao encontrado')
        except Exception as e:
           print(str(e))


    def run(self):
        self.__connect_socket()

        while True:
            try:
                cmd = input('> ')
                cmd_splited = cmd.split(' ')

                # self.server.sendall(cmd.encode())

                print('cmd_splited', cmd_splited)
                if cmd_splited[0].upper() == 'QUIT':
                    self.__desconnect_socket()
                elif cmd_splited[0].upper() == 'RETR':
                    self.__RETR(cmd)
                elif cmd_splited[0].upper() == 'STOR':
                    self.__STOR(cmd)

                # data = self.server.recv(1024)

                # if data:
                    # print(str(data.decode('utf-8')))

            except KeyboardInterrupt:
                self.__desconnect_socket()

        self.server.close()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 65432

    client = Client(HOST, PORT)
    client.run()

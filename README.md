### Servidor e cliente FTP

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Foi utilizado como referência a documentação [FTP](https://tools.ietf.org/html/rfc959).

### Depedências
* socket
* os
* sys
* threading  
* shutil
* pathlib 

#### Como usar?

Iniciando o servidor FTP.
```python
from FTP import FTPThread

if __name__ == "__main__":
    # Por padrão o servidor é executado em localhost
    HOST = 'localhost' 
    PORT = 65432

    tcp_server = Server(HOST, PORT)
    tcp_server.run()
```

Iniciando o servidor FTP.
```python
import Client

if __name__ == "__main__":
    # Conectando com o servidor criado anteriormente
    HOST = 'localhost'
    PORT = 65432

    client = Client(HOST, PORT)
    client.run()
```
**IMPORTANTE:** O host e a porta do cliente precisam ser a mesmas utilizadas para na criação do servidor.

### Executar
Executando script em Shell para iniciar servidor e cliente de forma automática forma automática.
```bash
git clone https://github.com/Marcusx11/TrabalhoRedes.git

cd TrabalhoRedes

chmod 777 run.sh && ./run.sh
```
Ou se preferir pode executar os arquivos de forma manual.
~~~bash
git clone https://github.com/Marcusx11/TrabalhoRedes.git

cd TrabalhoRedes

python3 src/server/main.py &&
python3 src/cliente/main.py
~~~

### Comandos
| Comandos       |    Descrição   |      
| :-------------   | :----------:   | 
|  RETR ou *get*   | Obtém uma cópia do arquivo especificado (download para o cliente).     | 
|  STOR ou *put*   | Envia uma cópia do arquivo especificado (upload para o servidor).   | 
|  DELE ou *rm*    | Apaga um arquivo   | 
|  MKD ou *mkdir*  | Cria um diretório.   | 
|  NLST ou *ls*    | Lista os nomes dos arquivos de um diretório.   | 
|  LIST ou *lsl*   | Retorna informações do arquivo ou diretório especificado (* ex.: nome tamanho, data de modificação, etc)  | 
|  QUIT ou *exit*  | Encerra a conexão com servidor  | 
|  HELP ou *?*  |Retorna documentação de uso (de um comando específico, se especificado; ou então um documento geral de ajuda). |

### Arquitetura
##### Estrutura de pastas
```
src
|  └───client
|     └── storage
│      main.py
└───server
|     └── storage
│      main.py
│      FTP.py
```


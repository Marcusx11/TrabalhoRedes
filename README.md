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

#### Arquitetura
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

### Executar
~~~
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
#!/bin/bash

## Para executar os programas servidor e cliente em janelas separadas
CMD_SRV='python3 src/server/main.py'
CMD_CLI='python3 src/client/main.py'

## Executando o servidor TCP
(xterm -hold -e $CMD_SRV || x-terminal-emulator -e $CMD_SRV) &

sleep 2

## Executando o cliente TCP
xterm -hold -e $CMD_CLI || x-terminal-emulator -e $CMD_CLI

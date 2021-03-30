import socket

#define o host e a porta da parte passiva ao qual a parte ativa irá se conectar
HOST = 'localhost'
PORT = 5000

#instancia o socket
socket_ativo = socket.socket()

#se coneta ao host e porta definidos acima
socket_ativo.connect((HOST, PORT))

while True:
    #recebe uma entrada de texto como mensagem
    msg = input()
    #envia a mensagem da entrada acima
    socket_ativo.send(str.encode(msg))
    #se a mensagem for 'fechar conexao', encerra o loop
    if msg == 'fechar conexao': break
    #recebe a mensagem da parte passiva
    print_msg = socket_ativo.recv(1024)
    #printa a mensagem recebida, ou seja, um echo da mensagem enviada
    print(str(print_msg, encoding = 'utf-8'))

#encerra o socket ativo e a conexão com a parte passiva
socket_ativo.close()
    

import socket

#define o host e a porta de conexão que a parte passiva irá receber conexões
HOST = ''
PORT = 5000

#instancia o socket
socket_passivo = socket.socket()

#define o host e a porta ao qual esse socket estará ouvindo
socket_passivo.bind((HOST, PORT))

# define o limite maximo de 5 conexoes pendentes e coloca-se em modo de espera por conexao
socket_passivo.listen(5)

#aceita uma conexão de socket, criando uma nova instancia de socket e recuperando o endereço de conexão
novo_socket, endereco = socket_passivo.accept()

while True:
    #espera até receber a mensagem em bytes (bloqueante)
    msg = novo_socket.recv(1024)
    #se a string recebida for 'fechar conexao', encerra o loop
    if str(msg, encoding='utf-8') == 'fechar conexao': break
    #reenvia a mensagem recebida
    novo_socket.send(msg)

#encerra o socket criado para a conexão com a parte ativa
novo_socket.close()

#encerra o socket principal
socket_passivo.close()
    

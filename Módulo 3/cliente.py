import socket

#define o host e a porta da parte passiva ao qual a parte ativa irá se conectar
HOST = 'localhost'
PORT = 5000

#instancia o socket
socket_ativo = socket.socket()

#se coneta ao host e porta definidos acima
socket_ativo.connect((HOST, PORT))

print("Conexão com servidor inicializada. Digite 'encerrar' para fechar conexão ou o nome do arquivo ao qual de deseja consultar.")

while True:
    #recebe uma entrada de texto como mensagem
    arquivo = input()
    #envia a mensagem da entrada acima
    socket_ativo.send(str.encode(arquivo))
    #encerra se for palavra chave
    if arquivo == 'encerrar' : break
    #recebe a mensagem do servidor
    palavras = socket_ativo.recv(1024)
    #printa a string recebida, podendo ser a ocorrencia das palavras ou que o arquivo não existe
    print(str(palavras, encoding = 'utf-8'))

#encerra o socket ativo e a conexão com o servidor
socket_ativo.close()

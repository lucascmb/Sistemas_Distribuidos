def AcessoDados(arquivo):

    import os.path

    #define a string que será o caminho para o arquivo na base de dados
    caminho = 'baseDados/' + arquivo + '.txt'

    #verifica se o arquivo existe
    resultado = os.path.exists(caminho)

    #caso exista, entra no if
    if resultado:

        #abre o arquivo para leitura
        f = open(caminho, 'r')

        #le todo o arquivo e o armazena na string palavras
        palavras = f.read()

        #fecha o arquivo
        f.close()

        #retorna a string contendo todo o conteudo do arquivo de forma crua
        return palavras

    #caso não exista, cai no else
    else:

        #retorna que o arquivo não existe
        return 'Arquivo não existe'


def Processamento(arquivo):

    import re

    #realiza o acesso a camada de dados
    _palavras = AcessoDados(arquivo)

    #se o arquivo não existir, retorna a camada de interface que não existe
    if (_palavras == 'Arquivo não existe'):

        return _palavras

    #substitui da string por um espaço em branco qualquer caracter que não for alfanumérico, além de tornar todas os caracteres para minusculo, a fim de melhor discernimento
    palavras = re.sub("[^0-9a-zA-Z]+", " ", _palavras).lower()

    #explode a string em uma lista com o separador sendo ' '
    lista = palavras.split(" ")

    #contorno para atribuir a d_lista um distinct da lista acima
    d_lista = list(set(lista))

    #define a variável que será a string de retorno como vazia
    retorno = ""

    #entra no loop para criar a string de retorno, iterando por toda a lista de palavras distintas no arquivo
    for i in range(0, len(d_lista)):

        #inicializa o contador em 0
        count = 0

        #conta o numero de ocorrencias da palavra que está no indice i da lista distinta na lista original
        count = lista.count(d_lista[i])

        #adiciona a string de retorno o numero de ocorrencias a palavra dessa iteração
        retorno += "Existem " + str(count) + " ocorrências de " + d_lista[i] + "\n"

    #retorna a string com o resultado a ser impresso
    return retorno


import socket

#define o host e a porta de conexão que a parte passiva irá receber conexões
HOST = ''
PORT = 5000

#instancia o socket
socket_passivo = socket.socket()

#define o host e a porta ao qual esse socket estará ouvindo
socket_passivo.bind((HOST, PORT))

# define o limite maximo de 1 conexão e coloca-se em modo de espera por conexao
socket_passivo.listen(1)

#aceita uma conexão de socket, criando uma nova instancia de socket e recuperando o endereço de conexão
novo_socket, endereco = socket_passivo.accept()

while True:
    #espera até receber a mensagem em bytes (bloqueante)
    msg = novo_socket.recv(1024)
    #transforma a mensagem
    arquivo = str(msg, encoding = 'utf-8')
    #caso receba a palavra chave entra no if
    if arquivo == "encerrar" :
        #encerra a conexão com a parte passiva
        novo_socket.close()
        #fica aguardando uma nova requisição de conexão no host:porta determinado previamente
        novo_socket, endereco = socket_passivo.accept()
    else:
        #chamada a camada de processamento
        retorno = Processamento(arquivo)
        #reenvia a mensagem recebida
        novo_socket.send(str.encode(retorno))
        

    

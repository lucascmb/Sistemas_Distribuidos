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
    from collections import Counter

    #realiza o acesso a camada de dados
    _palavras = AcessoDados(arquivo)

    #se o arquivo não existir, retorna a camada de interface que não existe
    if (_palavras == 'Arquivo não existe'):

        return _palavras

    #substitui da string por um espaço em branco qualquer caracter que não for alfanumérico, além de tornar todas os caracteres para minusculo, a fim de melhor discernimento
    palavras = re.sub("[^0-9a-zA-Z]+", " ", _palavras).lower()

    #explode a string em uma lista com o separador sendo ' '
    lista = palavras.split(" ")
    
    #cria uma lista de tuplas contendo a palavra e o numero de ocorrencias, ordenada da com maior numero de ocorrencias para a menor
    o_lista = Counter(lista).most_common()

    #define a variável que será a string de retorno como vazia
    retorno = ""

    #entra no loop para criar a string de retorno, iterando por toda a lista de palavras distintas no arquivo
    for i in range(0, len(o_lista)):
        
        #termina o for caso passe de 10 palavras
        if i == 10 : break

        #utilizando a lista ordenada, imprime da maior ocorrencia para a menor
        retorno += "Existem " + str(o_lista[i][1]) + " ocorrências de " + o_lista[i][0] + "\n"

    #retorna a string com o resultado a ser impresso
    return retorno


import socket
import sys
import select
import threading

#define o host e a porta de conexão que o servidor irá receber conexões
HOST = ''
PORT = 5000

#definição da lista de I/O que será aceita pelo servidor no comando select
entradas = [sys.stdin]

#dicionario para mapear as conexões do servidor com cada cliente (inicialmente vazio)
conexoes = {}

#Método para inicializar o servidor
def InicializaServidor():

    #instancia o socket
    server_socket = socket.socket()

    #define o host e a porta ao qual esse socket estará ouvindo
    server_socket.bind((HOST, PORT))

    #define o limite maximo de 1 conexão e coloca-se em modo de espera por conexao
    server_socket.listen(1)

    #define o socket como não bloqueante
    server_socket.setblocking(False)
    
    #inclui o socket principal na lista de entradas
    entradas.append(server_socket)
    
    #indica que o servidor foi inicializado
    print("Servidor inicializado e pronto para receber conexões com clientes.")
    print("Digite 'help' para exibir comando disponíveis.")
    
    return server_socket

def AceitaConexao(server_socket):
    
    #estabelece conexão com o cliente
    cliente_socket, endereco = server_socket.accept()
    
    #adiciona no dicionario de conexoes o endereço ligado ao socket da conexão com o cliente
    lock.acquire()
    conexoes[cliente_socket] = endereco
    lock.release()

def AtendeRequisicoes(cliente_socket, endereco):
    while True:
        #espera até receber a mensagem em bytes
        msg = cliente_socket.recv(1024)
        #transforma a mensagem
        arquivo = str(msg, encoding = 'utf-8')
        #caso receba a palavra chave entra no if
        if arquivo == "encerrar" :
            print("conexão encerrada com o cliente ", endereco)
            #encerra a conexão com o cliente
            cliente_socket.close()
            return
        else:
            #chamada a camada de processamento
            retorno = Processamento(arquivo)
            #reenvia a mensagem recebida
            cliente_socket.send(str.encode(retorno))
        

    
clientes = []

#Inicializa o servidor
server_socket = InicializaServidor()

while True:
    
    #espera por entradas, sejam elas conexões de clientes ou entradas de texto no próprio servidor
    leitura, escrita, excecao = select.select(entradas, [], [])
    
    for pronto in leitura :
        #se houver um pedido novo de conexão vindo de um cliente
        if pronto == server_socket:
            #estabelece conexão com o cliente, instanciando um novo socket
            cliente_socket, endereco = AceitaConexao(server_socket)
            
            print("Servidor conectado com : ", endereco)
            #cria uma nova thread (um novo fluxo) para atender as requisições do cliente com o qual a conexão foi estabelecida por socket
            thread_cliente = threading.Thread(target = AtendeRequisicoes, args = (cliente_socket, endereco))
            #inicializa a thread
            thread_cliente.start()
            
            clientes.append(thread_cliente)
        
        #se a entrada for um entrada padrão
        elif pronto == sys.stdin:
            
            comando = input()
            
            if comando == 'historico':
                print(str(conexoes.values()))
                
            elif comando == 'help' :
                print("digite 'encerrar servidor' para encerrar o servidor. \n Esse serviço passará a não receber mais conexões com novos clientes, porém só será finalizado após todos os clientes vigentes terem encerrado suas respectivas conexões.\n Também não irá receber mais comandos de entrada padrão.")
                print("digite 'historico' para exibir as conexões vigentes")    
                
            elif comando == 'encerra servidor':
                for c in clientes:
                    c.join()
                server_socket.close()
                sys.exit()


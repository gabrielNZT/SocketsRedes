import socket
import threading
import time

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []
mensagens = []
usuarios = []

def send(conexao):
    print(f"[SERVER] Enviando mensagens para {conexao['addr']}")
    for i in range(conexao['last'], len(mensagens)):
        mensagem_de_envio = "msg=" + mensagens[i]
        conexao['conn'].send(mensagem_de_envio.encode())
        conexao['last'] = i + 1
        time.sleep(0.2)

def sendAll():
    global conexoes
    for conexao in conexoes:
        send(conexao)

def sendUser(conexao):
    for i in range (len(usuarios)):
        mensagem_send = "msg="+"user "+str(i)+"=" + usuarios[i]
        conexao['conn'].send(mensagem_send.encode())
        time.sleep(0.2)

def sendUsuarios(addr):
    global conexoes
    for conexao in conexoes:
        if(conexao['addr'] == addr):
            for i in range (len(usuarios)): 
                mensagem_send = "msg="+"user "+str(i)+"=" + usuarios[i]
                conexao['conn'].send(mensagem_send.encode())
                time.sleep(0.2)

def removeClient(addr, nome):
    global conexoes
    global usuarios
    for conexao in conexoes:
        if(conexao['addr'] == addr):
            conexoes.remove(conexao)
    usuarios.remove(nome)
        
        
def handle_clientes(conn, addr):
    print(f"[SERVER] Um novo usuario se conectou pelo endereço {addr}")
    global conexoes
    global mensagens
    global usuarios
    nome = False

    while(1):
        msg = conn.recv(1024).decode(FORMATO)
        print(msg)
        if(msg):
            if(msg.startswith("nome=")):
                mensagem_separada = msg.split("=")            
                nome = mensagem_separada[1]
                mapa_da_conexao = {
                    "conn": conn,
                    "addr": addr,
                    "nome": nome,
                    "last": 0
                }
                conexoes.append(mapa_da_conexao)
                usuarios.append(mapa_da_conexao["nome"])
                send(mapa_da_conexao)
            elif(msg.startswith("msg=")):
                mensagem_separada = msg.split("=")
                mensagem = nome + "=" + mensagem_separada[1]
                if(mensagem_separada[1] == "/SAIR"):
                    removeClient(mapa_da_conexao["addr"], mapa_da_conexao["nome"])
                elif(mensagem_separada[1] == "/USUARIOS"):
                    sendUsuarios(mapa_da_conexao["addr"])
                else:
                    mensagens.append(mensagem)
                    sendAll()
                



def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while(True):
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()
from concurrent.futures import thread
import socket
import threading
import time

PORT = 5050
FORMATO = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

Porta = 0
ip = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
deseja_entrar = False

print(f"[CLIENT] Colinha para acessar o servidor (ip, porta): ", ADDR)

def handle_mensagens():
    while(True):
        msg = client.recv(1024).decode()
        mensagem_splitada = msg.split("=")
        print(mensagem_splitada[1] + ": " + mensagem_splitada[2])

def enviar(mensagem):   
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem():
    while(1):
        mensagem = input()
        enviar("msg=" + mensagem)

def enviar_nome():        
    nome = input('Digite seu nome: ')
    enviar("nome=" + nome)
                

def iniciar_envio():
    global deseja_entrar
    global ip
    global Porta
    while(not deseja_entrar):
         change = input("digite /ENTRAR parar entrar no chat: ")
         if(change == "/ENTRAR"):
             ip_input = input("informe o ip: ")
             ip = str(ip_input)
             Porta_input = input("informe a porta: ")
             Porta = int(Porta_input)
             addr = (ip, Porta)
             client.connect(addr)
             thread1 = threading.Thread(target=handle_mensagens)
             thread1.start()
             deseja_entrar = True

    enviar_nome()
    enviar_mensagem()

def iniciar():
    thread2 = threading.Thread(target=iniciar_envio)
    thread2.start()
    
iniciar()
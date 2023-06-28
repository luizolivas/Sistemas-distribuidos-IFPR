
from threading import Thread, Lock
import socket
from Restaurante import Restaurante
from Cliente import Cliente
from Cozinha import Cozinha

# Configurações do servidor
TCP_IP = '127.0.0.1'
TCP_PORT = 3216

# Criando uma instância do Restaurante (servidor) e da Cozinha
restaurante = Restaurante(TCP_IP, TCP_PORT)
cozinha = Cozinha()

def trata_cliente(conn, addr, restaurante):
    with conn:
        print(f'Servidor conectado por: {addr}')

        while True:
            data = conn.recv(1024)

            if not data:
                break

            mensagem = data.decode()
            print(f'Mensagem recebida: {mensagem} - do IP {addr[0]} : Porta {addr[1]}')

            restaurante.fazer_pedido(mensagem)
            resposta = f'Pedido recebido: {mensagem}'.encode()
            conn.sendall(resposta)
            print(f'Resposta enviada: {resposta.decode()} - para IP {addr[0]} : Porta {addr[1]}')


def iniciar_servidor(restaurante, tcp_ip, tcp_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((tcp_ip, tcp_port))
        sock.listen()

        print(f'Servidor inicializado em {tcp_ip}:{tcp_port}')

        while True:
            conn, addr = sock.accept()
            client_thread = Thread(target=trata_cliente, args=(conn, addr, restaurante))
            client_thread.start()


# Configurações do servidor
TCP_IP = '127.0.0.1'
TCP_PORT = 3216

# Criando uma instância do Restaurante (servidor) e da Cozinha
restaurante = Restaurante(TCP_IP, TCP_PORT)

# Iniciando o servidor em uma thread separada
server_thread = Thread(target=iniciar_servidor, args=(restaurante, TCP_IP, TCP_PORT))
server_thread.start()

# Criando uma instância do Cliente
cliente = Cliente(TCP_IP, TCP_PORT)

# Enviando um pedido do cliente para o servidor
cliente.enviar_pedido()

# Aguardando a finalização do servidor
server_thread.join()
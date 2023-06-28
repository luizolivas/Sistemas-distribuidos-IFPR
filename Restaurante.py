import socket
import threading
from threading import Thread, Semaphore, Lock
import time

from Cozinha import Cozinha

class Restaurante:
    def __init__(self, tcp_ip, tcp_port):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.cozinha = Cozinha()

    def organiza_pedido(self, pedido_recebido_cozinha: str):
        pedido_ok = pedido_recebido_cozinha.replace(',', ' pronto \n')
        return pedido_ok
    

    def trata_cliente(self, conn, addr):
        with conn:
            print(f'Servidor conectado por: {addr}')

            while True:
                data = conn.recv(1024)

                if not data:
                    break

                mensagem = data.decode()
                print(f'Mensagem recebida: {mensagem} - do IP {addr[0]} : Porta {addr[1]}')


                self.cozinha.receber_pedido(mensagem)

                pedido_pronto = self.cozinha.aguardar_pedido_pronto()
                pedido_pronto_organizado = self.organiza_pedido(pedido_pronto)


                conn.sendall(pedido_pronto_organizado.encode())

                print(f'Mensagem enviada: {pedido_pronto_organizado} - para IP {addr[0]} : Porta {addr[1]}')

    def iniciar_servidor(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.tcp_ip, self.tcp_port))
            sock.listen()

            print(f'Servidor inicializado em {self.tcp_ip}:{self.tcp_port}')

            while True:
                conn, addr = sock.accept()
                client_thread = threading.Thread(target=self.trata_cliente, args=(conn, addr))
                client_thread.start()

if __name__ == "__main__":
    # Configurações do servidor
    TCP_IP = '127.0.0.1'
    TCP_PORT = 3216

    restaurante = Restaurante(TCP_IP, TCP_PORT)

    server_thread = Thread(target=restaurante.iniciar_servidor)
    server_thread.start()

    server_thread.join()
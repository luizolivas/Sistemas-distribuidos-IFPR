from threading import Thread, Semaphore,Lock
import time


class Cozinha:
    def __init__(self):
        self.lock = Lock()
        self.semaforo = Semaphore(0)
        self.pedido_pronto = ''

    def receber_pedido(self, pedido):
        with self.lock:
            print("Pedido recebido na cozinha:", pedido)
            self.processar_pedido(pedido)

    def processar_pedido(self, pedido):
        itens = pedido.split(',')
        for item in itens:
            if item != '':
                print("Preparando item:", item)
                time.sleep(3)
                print("Item pronto:", item)
                self.pedido_pronto += item + ','
        self.semaforo.release()

    def aguardar_pedido_pronto(self):
        self.semaforo.acquire()
        with self.lock:
            pedido = self.pedido_pronto
            return pedido
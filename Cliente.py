import socket

IP = '127.0.0.1'
Server_Port = 3216

class Cliente:
    

    def __init__(self, nome) -> None:
        self.nome = nome
        self.pedido = ''
        self.cardapio = ["Carne", "Pizza", "Hambúrguer", "Lasanha", "Sushi"]

    def fazerPedido(self):
        cardapio = self.cardapio
        print("Escolha seu pedido: \n")
        decisao = True
        for i, item in enumerate(cardapio):
            print('( ' + str(i) + ' ) ' + item)
        
        while decisao == True:
            escolha = input('Digite o código da comida do cardápio (Ou digite 11 para fazer seu pedido): ')
            escolha = int(escolha) 

            if escolha == 11:
                decisao = False
                break
            else:
                self.pedido += cardapio[escolha] + ',' 
                print('\nComidas escolhidas:\n')
                print(self.pedido)



    def cliente_enviar_mensagem(self, IP, Server_Port):
        # Cria o socket padrão: IPv4 - TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print('Cliente Inicializado ...\n\n')

            # Conecta ao servidor
            sock.connect((IP, Server_Port))
            
            print('Cliente Conectado ao servidor ...\n\n')

            while True:
                self.fazerPedido()
                mensagem = self.pedido
                # Codifica a string para enviar ao servidor
                mensagem_codificada = mensagem.encode()

                # Envia a mensagem para o servidor
                sock.sendall(mensagem_codificada)

                print(f'Pedido: {mensagem} \n  - enviado para a cozinha, aguarde.\n')


                if mensagem == 'sair':
                    break

                # Aguarda/Recebe a mensagem de resposta do servidor
                data = sock.recv(1024)

                # Decodifica a mensagem retornando apenas a string referente à mensagem
                mensagem_resposta = data.decode()

                print(self.nome + f', Seu pedido está pronto, aqui está: ' + mensagem_resposta)
                self.pedido = ''




if __name__ == "__main__":
    IP = '127.0.0.1'
    Server_Port = 3216

    cliente = Cliente("Luiz")

    cliente.cliente_enviar_mensagem(IP, Server_Port)           




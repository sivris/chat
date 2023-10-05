"""
File contains the class that represents the server its initialization it.
"""
import socket
import threading


class Server:
    def __init__(self) -> None:
        # getting the local ip address
        self.HOST = socket.gethostbyname(socket.gethostname())  # 192.168.1.8
        self.PORT = 9090

        # creating the server socket and binding it with the address and the
        # port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))

        # server to listen mode (waiting for clients to connect)
        self.server.listen()
        print('_server is active_')

        # lists with clients and their nicknames
        self.clients = []
        self.nicknames = []

        # Start the server
        self.accept_clients()

        print('_server closed_')

    def broadcast(self, message, client_that_sent=None):
        """
        Method sends a message to all connected clients
        """
        for client in self.clients:
            if client_that_sent:
                if client_that_sent == client:
                    continue
                else:
                    client.send(message)
            else:
                client.send(message)

    def handle(self, client):
        """
        This method starts running every time a client connects to the server.
        It starts an endless loop that the server receives the messages from
        the client and then broadcasts these messages to every client using the
        broadcast method.
        """
        while True:
            index = self.clients.index(client)
            try:
                message = client.recv(1024)
                self.broadcast(message, client)

            except Exception:
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break

    def accept_clients(self):
        while True:
            # Accept the connection
            client, address = self.server.accept()

            # Sending to client "_give_nickname_ to get his nickname as
            # response"
            client.send('_give_nickname_'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            print(self.clients)

            # Broadcast to chat the new connection and notify user that is
            # connected to the server
            client.send('Connected to server!'.encode('utf-8'))
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

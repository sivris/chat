import socket
import threading


class Client:
    def __init__(self) -> None:
        # Define the host and the port
        self.HOST = '192.168.1.8'
        self.PORT = 9090

        # Client choosing nickname
        self.nickname = self.choose_nickname()

        # Connecting to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

        self.receive()

    def receive(self):
        while True:
            try:
                # Receiving message from server
                message = self.client_socket.recv(1024).decode('utf-8')

                # Checking if the message is the trigger for the nickname
                if message == '_give_nickname_':
                    self.client_socket.send(self.nickname.encode('utf-8'))

                else:
                    print(message)

            except Exception as e:
                print(e)

                # Close the connection if something occurs
                print('Something went wrong!')
                self.client_socket.close()
                break

    def choose_nickname(self) -> str:
        """
        Method for client's nickname
        """
        while True:
            nickname = input('Pick your nickname: ')

            while True:
                print(f'Your nickname is: {nickname}')
                response = input(
                    'Press Y to continue or N to choose new nickname:'
                    ).capitalize()

                if response == 'Y':
                    return nickname

                elif response == 'N':
                    break

                else:
                    print('Try again..')
                    continue

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client_socket.send(message.encode('utf-8'))

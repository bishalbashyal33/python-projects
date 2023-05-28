import socket
import threading

# Function to handle receiving messages
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            print(data)
        except:
            break

# Function to handle sending messages
def send_message(sock, username):
    while True:
        message = input("You:")
        formatted_message = f"\n{username}: {message}"
        sock.send(formatted_message.encode('utf-8'))

# Function to start the server
def start_server(port):
    server_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_sock.bind(('::', port))
    server_sock.listen(1)
    print('Server started, waiting for connections...')

    client_sock, client_addr = server_sock.accept()
    print('Connected to', client_addr[0])

    # Get usernames from client and server
    server_username = input('Enter your username (server): ')
    client_username = client_sock.recv(1024).decode('utf-8')
    client_sock.send(server_username.encode('utf-8'))

    # Start receiving and sending messages in separate threads
    receive_thread = threading.Thread(target=receive_messages, args=(client_sock,))
    send_thread = threading.Thread(target=send_message, args=(client_sock, server_username))
    receive_thread.start()
    send_thread.start()

# Function to establish a connection as a client
def establish_connection(ip, port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print('Connected to', ip)

    # Get usernames from client and server
    client_username = input('Enter your username (client): ')
    sock.send(client_username.encode('utf-8'))
    server_username = sock.recv(1024).decode('utf-8')

    # Start receiving and sending messages in separate threads
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    send_thread = threading.Thread(target=send_message, args=(sock, client_username))
    receive_thread.start()
    send_thread.start()

# Entry point
if __name__ == '__main__':
    option = input('Choose an option: (1) Start as server, (2) Connect as client: ')

    if option == '1':
        port = int(input('Enter the port number to start the server: '))
        start_server(port)
    elif option == '2':
        ipv6 = input('Enter the IPv6 address of the server: ')
        port = int(input('Enter the port number: '))
        establish_connection(ipv6, port)
    else:
        print('Invalid option. Please try again.')

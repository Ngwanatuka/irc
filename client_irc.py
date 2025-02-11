import socket

def start_client():
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to the server. Type your commands below.")
    while True:
        command = input()
        if command.lower() == 'quit':
            break
        client_socket.send(command.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response.strip())

    client_socket.close()

if __name__ == '__main__':
    start_client()
import socket
import threading
import os

# Server configuration
HOST = os.getenv('IRC_HOST')
PORT = int(os.getenv('IRC_PORT'))

# Store connected clients and channels
clients = {}
channels = {}

def handle_client(client_socket):
    """Handle communication with a connected client."""
    nick = None
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Parse IRC commands
            if data.startswith('NICK'):
                nick = data.split()[1]
                clients[client_socket] = nick
                client_socket.send(f':Welcome, {nick}!\r\n'.encode('utf-8'))
            elif data.startswith('JOIN'):
                channel = data.split()[1]
                if channel not in channels:
                    channels[channel] = []
                channels[channel].append(client_socket)
                client_socket.send(f':{nick} joined {channel}\r\n'.encode('utf-8'))
            elif data.startswith('PRIVMSG'):
                _, target, message = data.split(' ', 2)
                if target.startswith('#'):  # Channel message
                    for client in channels.get(target, []):
                        client.send(f':{nick} {message}\r\n'.encode('utf-8'))
                else:  # Private message
                    for sock, name in clients.items():
                        if name == target:
                            sock.send(f':{nick} {message}\r\n'.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if nick:
            del clients[client_socket]
        client_socket.close()

def start_server():
    """Start the IRC server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    start_server()
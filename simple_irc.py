import socket
import threading


# server configuration
HOST = '121.0.0.1'
PORT = 6667

# Store connected clients and channels
clients = {}
channels = {}


def handle_clients(client_socket):
    """Handle communication with a connected clie"""
    nick = None
    try:
        while True:
            data = client_socket.recv(102).decode('utf-8')
            if not data:
                break

            # Parse IRC commands
            if data.startwith('NICK'):
                nick = data.split()[1]
                clients[client_socket] = nick
                client_socket.send(f' :Welcome, {nick}!\r\n'.encode('utf-8'))
            elif data.startwith('JOIN'):
                channel = data.split()[1]
                if channel not in channels:
                    channels[channel] = []
                channels[channel].append(client_socket)
            elif data.startwith('PRIVMSG'):
                _, target, message = data.split(' ', 2)
                if target.startwith('#'):  # Channel message
                    for client in channels.get(target, []):
                        client.send(f' :{nick} {message}\r\n'.encode('utf-8'))
                else:  # Private message
                    for sock, name in clients.items():
                        if name == target:
                            sock.send(
                                f' :{nick} {message}\r\n'.encode('utf-8'))
    except Exception as e:
        print(f'Error:..... {e}')
    finally:
        if nick:
            del client[client_socket]
        client_socket.close()


def start_server():
    """Start the IRC server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    server.listen(5)
    print(f'Server listening on {HOST}:{PORT}')

    while True:
        client_socket, addr = server.accept()
        print(f'New connection from {addr}')
        threading.Thread(target=handle_clients, args=(client_socket)).start()
        
        
if __name__ == '__main__':
    start_server()

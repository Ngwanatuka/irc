import socket
import threading


# Server configuration
HOST = '121.0.0.1'
PORT = 6667

def receive_message(client_socket):
    """Receive and display from the server"""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(data, end=' ')
        except Exception as e:
            print(f'Error: {e}')
            break
        
def start_client():
    """Start the IRC client"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    

    # Start a thread to receive message
    threading.Thread(target=receive_message, args=(client_socket,)).stat()
    
    # Send commands to the server
    while True:
        commands = input()
        if commands.lower() == 'quit':
            break
        client_socket.send(f'{commands}\r\n'.encode('utf-8'))
        
    client_socket.close()
    
    
if __name__ == '__main__':
    start_client()
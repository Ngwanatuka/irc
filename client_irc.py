import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Ensure this matches the server's HOST
PORT = 6667         # Ensure this matches the server's PORT

def receive_messages(client_socket):
    """Receive and display messages from the server."""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(data, end='')
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def start_client():
    """Start the IRC client."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Attempting to connect to {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected to the server!")

        # Start a thread to receive messages
        threading.Thread(target=receive_messages, args=(client_socket,)).start()

        # Send commands to the server
        while True:
            command = input()
            if command.lower() == 'quit':
                break
            client_socket.send(f'{command}\r\n'.encode('utf-8'))

    except Exception as e:
        print(f"Failed to connect to the server: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == '__main__':
    start_client()
import socket
import threading

# Server configuration
HOST = '20.20.21.6'
PORT = 6667

def listen_for_messages(client_socket):
    """Listen for messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

def send_messages(client_socket):
    """Send messages to the server."""
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def main():
    """Main function to connect to the server and start listening and sending threads."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Start a thread to listen for messages from the server
    threading.Thread(target=listen_for_messages, args=(client_socket,)).start()

    # Start a thread to send messages to the server
    threading.Thread(target=send_messages, args=(client_socket,)).start()

if __name__ == '__main__':
    main()

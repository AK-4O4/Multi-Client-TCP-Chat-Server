import socket
import threading
import sys

HOST = '127.0.0.1' 
PORT = 5555

def receive_messages(client_socket):
    """This thread constantly listens for messages from the server."""
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\n[!] Server closed the connection.")
                client_socket.close()
                sys.exit()
            
            # Print the message and a new prompt so it looks clean
            print(f"\r{data.decode('utf-8')}\n> ", end="")
            
        except:
            print("\n[!] Lost connection to server.")
            client_socket.close()
            sys.exit()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[*] Connected to {HOST}:{PORT}")
    print("> ", end="")
    
    # 1. Start the receiving thread in the background
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    recv_thread.start()
    
    # 2. Main thread handles sending
    while True:
        message = input("") # Wait for user to type
        if message.lower() == 'quit':
            break
        
        client_socket.sendall(message.encode('utf-8'))
        
    client_socket.close()

if __name__ == "__main__":
    start_client()
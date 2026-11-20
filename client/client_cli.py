import socket

HOST = '127.0.0.1'  # Localhost
PORT = 5555

def start_client():
    # 1. Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Connect to server
    client_socket.connect((HOST, PORT))
    print(f"[*] Connected to server at {HOST}:{PORT}")
    
    while True:
        message = input("Type a message (or 'quit' to exit): ")
        if message.lower() == 'quit':
            break
            
        # 3. Send data
        client_socket.sendall(message.encode('utf-8'))
        
        # 4. Receive echo
        data = client_socket.recv(1024)
        print(f"[Echo] {data.decode('utf-8')}")
        
    client_socket.close()

if __name__ == "__main__":
    start_client()
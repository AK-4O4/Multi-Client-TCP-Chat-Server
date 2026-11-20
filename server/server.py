import socket

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5555

def start_server():
    # 1. Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Bind to host and port
    server_socket.bind((HOST, PORT))
    
    # 3. Listen for connections
    server_socket.listen(1)
    print(f"[*] Echo Server listening on {HOST}:{PORT}")
    
    # 4. Accept a connection
    conn, addr = server_socket.accept()
    print(f"[*] Connected by {addr}")
    
    while True:
        # 5. Receive data (up to 1024 bytes)
        data = conn.recv(1024)
        if not data:
            break # Client disconnected
            
        print(f"[Client] {data.decode('utf-8')}")
        
        # 6. Send the exact same data back (Echo)
        conn.sendall(data)
        
    # 7. Clean up
    conn.close()
    server_socket.close()
    print("[*] Connection closed.")

if __name__ == "__main__":
    start_server()
import socket
import threading

HOST = '0.0.0.0'
PORT = 5555

# This list holds the sockets of all connected clients
clients = []

# The lock ensures that only one thread can modify the 'clients' list at a time
# This prevents race conditions!
lock = threading.Lock()

def broadcast(message, sender_socket):
    """Sends a message to every connected client except the sender."""
    # We iterate over a copy of the list (clients[:]) so we don't crash 
    # if a client disconnects while we are looping
    with lock:
        current_clients = clients[:]
        
    for client in current_clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                # If sending fails, the client is probably dead. Remove them.
                with lock:
                    if client in clients:
                        clients.remove(client)
                client.close()

def handle_client(conn, addr):
    """This function runs in a separate thread for every single client."""
    print(f"[+] New connection from {addr}")
    
    # Add the new client to our shared list
    with lock:
        clients.append(conn)
        
    try:
        while True:
            # Wait for data from this specific client
            data = conn.recv(1024)
            if not data:
                break # Client disconnected normally
            
            # Decode and format the message (We'll use a dummy name for Week 11)
            text = data.decode('utf-8')
            message = f"[{addr[1]}]: {text}".encode('utf-8')
            
            print(f"Broadcasting: {text}")
            broadcast(message, conn)
            
    except ConnectionResetError:
        print(f"[-] {addr} abruptly disconnected")
    finally:
        # CLEANUP: This runs even if the client crashes
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"[-] Connection closed for {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print(f"[*] Multi-threaded Server listening on {HOST}:{PORT}")
    
    while True:
        # 1. Wait for a new connection
        conn, addr = server_socket.accept()
        
        # 2. Spawn a new worker thread for this client
        # daemon=True means the thread will die if the main program exits
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
        print(f"[*] Active threads: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
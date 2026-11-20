import socket
import threading

HOST = '0.0.0.0'
PORT = 5555

# Shared Data: maps socket objects to nicknames
clients = {}
lock = threading.Lock()

def broadcast(message):
    """Sends a message to ALL connected clients."""
    with lock:
        current_sockets = list(clients.keys())
        
    for sock in current_sockets:
        try:
            sock.sendall(message)
        except:
            pass

def handle_client(conn, addr):
    """This function runs in a separate thread for EVERY client."""
    nick = None
    try:
        # 1. Ask for a nickname upon connection
        conn.sendall("Enter your nickname: ".encode('utf-8'))
        nick = conn.recv(1024).decode('utf-8').strip()
        
        # 2. Check if nickname is taken
        with lock:
            if nick in clients.values():
                conn.sendall("Error: Nickname already in use. Disconnecting.\n".encode('utf-8'))
                return # Exits, triggering the finally block
            
            clients[conn] = nick
        
        # 3. Announce the new user (Send to EVERYONE)
        broadcast(f"[Server] * {nick} has joined the chat.\n".encode('utf-8'))
        print(f"[+] {nick} connected from {addr}")

        # 4. Main loop to receive messages
        while True:
            data = conn.recv(1024)
            if not data:
                break 
            
            text = data.decode('utf-8')
            
            # --- COMMAND PARSING ---
            if text.startswith('/nick '):
                new_nick = text.split(' ', 1)[1].strip()
                with lock:
                    if new_nick in clients.values():
                        conn.sendall("Error: That nickname is already taken.\n".encode('utf-8'))
                    else:
                        old_nick = clients[conn]
                        clients[conn] = new_nick
                        nick = new_nick
                        # Send to EVERYONE
                        broadcast(f"[Server] * {old_nick} is now known as {new_nick}.\n".encode('utf-8'))
            
            elif text.startswith('/msg '):
                # ... (Keep the /msg code exactly the same, it only goes to one person) ...
                parts = text.split(' ', 2)
                if len(parts) == 3:
                    target_nick, msg = parts[1], parts[2]
                    with lock:
                        target_sock = next((s for s, n in clients.items() if n == target_nick), None)
                    
                    if target_sock:
                        target_sock.sendall(f"[PM from {nick}] {msg}\n".encode('utf-8'))
                    else:
                        conn.sendall(f"Error: User '{target_nick}' not found.\n".encode('utf-8'))
            
            elif text.lower() == '/quit':
                break
            
            else:
                # Standard broadcast (Send to EVERYONE)
                broadcast(f"[{nick}] {text}\n".encode('utf-8'))

    except ConnectionResetError:
        pass 
    finally:
        # ... (Keep the cleanup exactly the same) ...
        with lock:
            if conn in clients:
                del clients[conn]
        conn.close()
        
        if nick:
            broadcast(f"[Server] * {nick} has left the chat.\n".encode('utf-8'))
            print(f"[-] {nick} disconnected.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    print(f"[*] Server listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server_socket.accept()
        # Spawn a new thread for the client
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()
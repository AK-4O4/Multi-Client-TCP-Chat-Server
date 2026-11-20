# Multi-Client TCP Chat Server

**Course:** Parallel and Distributed Computing
**Project Target:** TCP sockets, client–server with one thread per client.  
**Data Task:** Receives, routes, and broadcasts message data among many clients on different lab PCs.

## 📌 Project Overview
This project is a fully functional, concurrent chat application built entirely from scratch using Python's standard networking and threading libraries. It uses sockets to demonstrate a fundamental understanding of parallel I/O, thread coordination, and shared-state management in a distributed environment.

### Key Features
*   **Concurrent Connections:** Supports multiple clients simultaneously using a Thread-per-Client architecture.
*   **Thread Safety:** Utilizes `threading.Lock()` to protect shared data structures from race conditions.
*   **Command Routing:**
    *   `/nick <name>`: Change display name (with duplicate prevention).
    *   `/msg <name> <text>`: Send private messages directly to a specific user.
    *   `/quit`: Gracefully disconnect from the server.
    *   Any standard text is broadcasted to all connected users.
*   **Fault Tolerance:** Handles sudden client disconnects (e.g., closing the window or network drop) without crashing the server.

---

## 🏗️ Architecture

1.  **Framework (TCP Sockets):** The server uses `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` to establish a reliable, connection-oriented transport layer.
2.  **Data Task (Routing & Broadcasting):** The server receives byte streams, parses them into commands, and uses a shared dictionary `{socket: nickname}` to route private messages or broadcast public messages.
3.  **Work Split (Thread-per-Client):** The main server thread sits at `accept()`. Once a client connects, the server spawns a dedicated worker thread `threading.Thread(target=handle_client)`. This prevents blocking I/O from one client freezing the entire server.
4.  **Coordination (Shared Data & Locks):** Because multiple threads read and write to the `clients` dictionary simultaneously, a `threading.Lock()` is used to create a critical section, preventing `RuntimeError` (dictionary changed size during iteration) and data corruption.

---
## 🖥️ To Run

#### **1. Start the Server:** In the terminal, run:
```bash
python server/server.py
```
#### **1. Start the Server:** Open a new terminal (or multiple terminals for multiple local users), activate the environment, and run:
```bash
python client/client_gui.py
```
#### **3. Connecting Across Multiple Connected PCs (Distributed Setup):** To connect clients from different computers on the same network:
1. On the Server PC, open your terminal and find your IPv4 address using ipconfig (e.g., 192.168.1.15).
2. On the Client PC, open client/client_gui.py in a text editor.
3. Scroll to line 12 and change the IP address:
```python
SERVER_IP = '192.168.1.15' # Change from 127.0.0.1 to your Server's IP
```
4. Run the client script:
```bash
python client/client_gui.py
```
(Note: Ensure Windows Firewall on the Server PC allows incoming connections on port 5555).

---

## 📂 Directory Structure

```text
PDC_Chat_Server/
│
├── client/
│   ├── client_cli.py       # Basic command-line client (for testing)
│   └── client_gui.py       # Main GUI client (CustomTkinter)
│
├── server/
│   └── server.py           # Multi-threaded TCP Server
│
├── docs/
│   ├── commands.md         # Week 10 Command Proposal
│   └── test_log.md         # Week 13 Testing results
│
├── .gitignore
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

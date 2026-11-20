import socket
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sys

# --- CONFIGURATION ---
# Change this to the SERVER'S IP address for the live demo on lab PCs!
SERVER_IP = '127.0.0.1' 
PORT = 5555

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("PDC Chat App")
        self.root.geometry("500x600")
        ctk.set_appearance_mode("Dark")
        
        # --- NETWORKING SETUP ---
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((SERVER_IP, PORT))
            # Server immediately asks for nickname
            self.sock.recv(1024).decode('utf-8') 
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to server at {SERVER_IP}:{PORT}")
            sys.exit()

        # --- LOGIN PROMPT ---
        self.nick = ctk.CTkInputDialog(text="Enter your nickname:", title="Login").get_input()
        if not self.nick:
            sys.exit()
        self.sock.sendall(self.nick.encode('utf-8'))

        # --- GUI SETUP ---
        # Chat Area
        self.chat_area = ctk.CTkTextbox(root, width=480, height=480, state="disabled")
        self.chat_area.pack(pady=10, padx=10)

        # Bottom Frame for Input
        self.bottom_frame = ctk.CTkFrame(root)
        self.bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.msg_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Type message, /msg <user> <text>, /nick <name>...")
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_btn = ctk.CTkButton(self.bottom_frame, text="Send", width=80, command=self.send_message)
        self.send_btn.pack(side="right")

        # --- START RECEIVING THREAD ---
        # This thread runs in the background so the GUI doesn't freeze
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # Update GUI safely from the background thread
                self.chat_area.configure(state="normal")
                self.chat_area.insert(tk.END, data)
                self.chat_area.see(tk.END) # Auto-scroll to bottom
                self.chat_area.configure(state="disabled")
            except:
                break # Disconnected

        # If loop breaks, connection lost
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, "\n[!] Connection closed by server.")
        self.chat_area.configure(state="disabled")
        self.send_btn.configure(state="disabled")

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return

        if msg.lower() == "/quit":
            self.sock.sendall(msg.encode('utf-8'))
            self.root.quit()
            return

        try:
            self.sock.sendall(msg.encode('utf-8'))
            self.msg_entry.delete(0, tk.END)
        except:
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.configure(placeholder_text="Disconnected from server.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatClient(root)
    root.mainloop()
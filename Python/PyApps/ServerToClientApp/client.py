#!/usr/bin/env python3

import socket
import threading
import customtkinter as ctk

# Clase principal de la aplicación cliente
class ChatCliente(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat Cliente")
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables de conexión
        self.client_socket = None
        self.nombre_usuario = None

        # Interfaz de login
        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.pack(pady=100)
        self.label_nombre = ctk.CTkLabel(self.frame_login, text="Nombre de usuario:")
        self.label_nombre.pack(pady=10)
        self.entry_nombre = ctk.CTkEntry(self.frame_login)
        self.entry_nombre.pack(pady=10)
        self.boton_conectar = ctk.CTkButton(self.frame_login, text="Conectar", command=self.conectar)
        self.boton_conectar.pack(pady=10)

        # Interfaz de chat (inicialmente oculta)
        self.frame_chat = ctk.CTkFrame(self)
        self.texto_chat = ctk.CTkTextbox(self.frame_chat, width=350, height=300, state="disabled")
        self.entry_mensaje = ctk.CTkEntry(self.frame_chat, width=250)
        self.boton_enviar = ctk.CTkButton(self.frame_chat, text="Enviar", command=self.enviar_mensaje)

    # Función para conectar al servidor
    def conectar(self):
        self.nombre_usuario = self.entry_nombre.get()
        if not self.nombre_usuario:
            ctk.CTkMessagebox(title="Error", message="Introduce un nombre de usuario.", icon="warning")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))
            self.client_socket.sendall(self.nombre_usuario.encode('utf-8'))
            self.frame_login.pack_forget()
            self.frame_chat.pack(pady=10)
            self.texto_chat.pack(pady=10)
            self.entry_mensaje.pack(side="left", padx=10)
            self.boton_enviar.pack(side="left")
            threading.Thread(target=self.recibir_mensajes, daemon=True).start()
        except Exception as e:
            ctk.CTkMessagebox(title="Error", message=f"No se pudo conectar: {e}", icon="warning")

    # Función para enviar mensajes al servidor
    def enviar_mensaje(self):
        mensaje = self.entry_mensaje.get()
        if mensaje and self.client_socket:
            try:
                self.client_socket.sendall(mensaje.encode('utf-8'))
                self.texto_chat.configure(state="normal")
                self.texto_chat.insert("end", f"Tú: {mensaje}\n")
                self.texto_chat.configure(state="disabled")
                self.entry_mensaje.delete(0, "end")
            except Exception as e:
                self.texto_chat.configure(state="normal")
                self.texto_chat.insert("end", f"[Error al enviar]: {e}\n")
                self.texto_chat.configure(state="disabled")

    # Función para recibir mensajes del servidor
    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.client_socket.recv(1024)
                if not mensaje:
                    break
                mensaje_decodificado = mensaje.decode('utf-8')
                self.texto_chat.configure(state="normal")
                self.texto_chat.insert("end", f"{mensaje_decodificado}\n")
                self.texto_chat.configure(state="disabled")
            except Exception as e:
                self.texto_chat.configure(state="normal")
                self.texto_chat.insert("end", f"[Desconectado]: {e}\n")
                self.texto_chat.configure(state="disabled")
                break

if __name__ == "__main__":
    app = ChatCliente()
    app.mainloop()
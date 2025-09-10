#!/usr/bin/env python3

import socket
import threading

# Diccionario para guardar los nombres de usuario
usuarios = {}
# Lista para guardar los sockets de los clientes conectados
clientes = []

# Función que maneja la comunicación con cada cliente
def manejar_cliente(client_socket):
    try:
        # Recibe el nombre de usuario
        nombre = client_socket.recv(1024).decode('utf-8')
        usuarios[client_socket] = nombre
        print(f"[+] Usuario conectado: {nombre}")

        while True:
            mensaje = client_socket.recv(1024)
            if not mensaje:
                break
            mensaje_decodificado = mensaje.decode('utf-8')
            print(f"[{nombre}] {mensaje_decodificado}")
            # Reenvía el mensaje a todos los clientes
            for c in clientes:
                if c != client_socket:
                    try:
                        c.sendall(f"{nombre}: {mensaje_decodificado}".encode('utf-8'))
                    except:
                        pass
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print(f"[-] Usuario desconectado: {usuarios.get(client_socket, '')}")
        clientes.remove(client_socket)
        client_socket.close()
        usuarios.pop(client_socket, None)

def iniciar_servidor():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print("[*] Servidor escuchando en puerto 12345...")

    while True:
        client_socket, addr = server_socket.accept()
        clientes.append(client_socket)
        print(f"[+] Conexión desde {addr}")
        thread = threading.Thread(target=manejar_cliente, args=(client_socket,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
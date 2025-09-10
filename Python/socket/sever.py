import socket

# Crear el socket TCP (IPv4, TCP)
server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Asignar IP y puerto
server_socket.bind(("127.0.0.1", 12345))

# Escuchar conexiones (máx. 1 en cola)
server_socket.listen(1)
print("Servidor esperando conexiones...")

# Aceptar conexión
conn, addr = server_socket.accept()
print(f"Conectado con {addr}")

# Recibir y responder
while True:
    data = conn.recv(1024)  # recibe 1024 bytes
    if not data:
        break
    print("Cliente:", data.decode())
    respuesta = input("Servidor >> ")
    conn.sendall(respuesta.encode())

# Cerrar conexión
conn.close()
server_socket.close()

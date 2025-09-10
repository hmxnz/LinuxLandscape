import socket

# Crear socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
client_socket.connect(("127.0.0.1", 12345))
print("Conectado al servidor.")

# Enviar y recibir mensajes
while True:
    mensaje = input("Cliente >> ")
    client_socket.sendall(mensaje.encode())
    data = client_socket.recv(1024)
    print("Servidor:", data.decode())

import socket
import threading

# Función que manejará cada cliente en un hilo
def manejar_cliente(conn, addr):
    print(f"[+] Nueva conexión: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Cliente {addr}: {data.decode()}")
            respuesta = f"Servidor recibió: {data.decode()}"
            conn.sendall(respuesta.encode())
        except:
            break
    print(f"[-] Cliente {addr} desconectado")
    conn.close()

def main():
    # Crear socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))
    server_socket.listen(5)  # hasta 5 conexiones en cola
    print("[*] Servidor escuchando en 127.0.0.1:12345")

    while True:
        conn, addr = server_socket.accept()
        # Crear un hilo para cada cliente
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()
        print(f"[!] Conexiones activas: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()

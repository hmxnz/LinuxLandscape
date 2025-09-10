# Chat Cliente-Servidor con Interfaz Gráfica

Este proyecto es una aplicación de chat en tiempo real que permite la comunicación entre varios clientes conectados a un servidor central. La interfaz gráfica del cliente está desarrollada con [customtkinter](https://github.com/TomSchimansky/CustomTkinter), ofreciendo una experiencia moderna y atractiva.

---

## Características

- Comunicación en tiempo real entre múltiples clientes.
- Interfaz gráfica amigable y personalizable.
- Código comentado para facilitar el aprendizaje.
- Fácil de ejecutar en cualquier sistema con Python 3.

---

## Requisitos

- **Python 3.8 o superior**
- **customtkinter**  
  Instala customtkinter en un entorno virtual para evitar problemas con el sistema:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install customtkinter
  ```

---

## Estructura de archivos

```
ServerToClientApp/
├── client.py      # Cliente con interfaz gráfica
├── server.py      # Servidor que gestiona los mensajes
└── README.md      # Este archivo
```

---

## Cómo ejecutar el proyecto

1. **Clona el repositorio o copia los archivos en una carpeta.**

2. **Instala las dependencias en un entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install customtkinter
   ```

3. **Inicia el servidor:**
   ```bash
   python server.py
   ```

4. **Inicia uno o varios clientes (en diferentes terminales):**
   ```bash
   python client.py
   ```

5. **En la ventana del cliente, introduce tu nombre de usuario y comienza a chatear.**

---

## Funcionamiento

- El **servidor** escucha conexiones en el puerto `12345` y gestiona los mensajes entre los clientes.
- Cada **cliente** se conecta al servidor, envía su nombre de usuario y puede enviar/recibir mensajes en tiempo real.
- Los mensajes enviados por un cliente se muestran en la ventana de todos los clientes conectados.

---

## Notas

- El proyecto no incluye cifrado de mensajes por defecto. Si deseas añadir cifrado, puedes usar la librería `cryptography` y modificar el código siguiendo las recomendaciones de la documentación.
- Para ejecutar varios clientes en la misma máquina, abre varias terminales y ejecuta `client.py` en cada una.
- Próximamente subiré la verion 1.1 de la aplicación la caul incorporará el sistema de cifrado de mensajes para simular un sistema de mensajes encriptado.
---

## Autor

Desarrollado por Hugo Martínez Segura
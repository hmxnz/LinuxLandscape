# nota.py
import datetime

class Nota:
    """
    Clase que representa una nota individual.
    Cada nota tiene título, contenido, fecha de creación y un id único.
    """
    contador_id = 1  # Contador de IDs para asignar automáticamente

    def __init__(self, titulo, contenido):
        self.id = Nota.contador_id
        self.titulo = titulo
        self.contenido = contenido
        self.fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        Nota.contador_id += 1  # Incrementar contador global de IDs

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.fecha})\n{self.contenido}\n"

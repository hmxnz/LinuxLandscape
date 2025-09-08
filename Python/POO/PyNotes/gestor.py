# gestor.py
import pickle
import os
from nota import Nota

class GestorNotas:
    """
    Clase que gestiona una colección de notas.
    Soporta crear, listar, buscar y eliminar notas, con persistencia en disco usando Pickle.
    """
    def __init__(self, archivo="data.pkl"):
        self.archivo = archivo
        self.notas = self.cargar_notas()

    def guardar_notas(self):
        """
        Guarda las notas en disco usando Pickle.
        """
        with open(self.archivo, "wb") as f:
            pickle.dump(self.notas, f)

    def cargar_notas(self):
        """
        Carga las notas desde disco (si existen).
        """
        if os.path.exists(self.archivo):
            with open(self.archivo, "rb") as f:
                return pickle.load(f)
        return []

    def crear_nota(self, titulo, contenido):
        """
        Crea una nueva nota y la guarda.
        """
        nota = Nota(titulo, contenido)
        self.notas.append(nota)
        self.guardar_notas()
        print("✅ Nota creada con éxito.")

    def listar_notas(self):
        """
        Muestra todas las notas existentes.
        """
        if not self.notas:
            print("No hay notas guardadas.")
        for nota in self.notas:
            print(nota)

    def buscar_notas(self, criterio):
        """
        Busca notas por título o contenido que contengan el criterio.
        """
        resultados = [n for n in self.notas if criterio.lower() in n.titulo.lower() or criterio.lower() in n.contenido.lower()]
        if resultados:
            for nota in resultados:
                print(nota)
        else:
            print("No se encontraron notas con ese criterio.")

    def eliminar_nota(self, id_nota):
        """
        Elimina una nota por su ID.
        """
        for nota in self.notas:
            if nota.id == id_nota:
                self.notas.remove(nota)
                self.guardar_notas()
                print("🗑️ Nota eliminada con éxito.")
                return
        print("No se encontró ninguna nota con ese ID.")

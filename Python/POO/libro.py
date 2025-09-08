class Libro:

    def __init__(self, titulo, autor, anio_publicacion, prestado=False):
        self.titulo = titulo
        self.autor = autor
        self.anio_publicacion = anio_publicacion
        self.prestado = prestado

    def descripcion(self):
        return f"'{self.titulo}' por {self.autor}, publicado en {self.anio_publicacion}"

    def prestar(self):
        if not self.prestado:
            self.prestado = True
            print(f"El libro '{self.titulo}' ha sido prestado.")
        else:
            print(f"El libro '{self.titulo}' ya está prestado.")

    def devolver(self):
        if self.prestado:
            self.prestado = False
            print(f"El libro '{self.titulo}' ha sido devuelto.")
        else:
            print(f"El libro '{self.titulo}' no estaba prestado.")

    def __str__(self):
        estado = "Prestado" if self.prestado else "Disponible"
        return f"'{self.titulo}' por {self.autor} ({self.anio_publicacion}) - {estado}"


class Biblioteca:

    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []

    def agregar_libro(self, libro):
        self.catalogo.append(libro)
        print(f"El libro '{libro.titulo}' ha sido agregado a la biblioteca.")

    def mostrar_libros(self):
        if not self.catalogo:
            print("No hay libros en la biblioteca.")
            return
        for libro in self.catalogo:
            print(libro)

    def buscar_libro_por_autor(self, autor):
        encontrados = [libro for libro in self.catalogo if libro.autor.lower() == autor.lower()]
        if encontrados:
            return encontrados
        print(f"No se encontraron libros del autor '{autor}'.")
        return []

    def prestar_libro(self, titulo):
        for libro in self.catalogo:
            if libro.titulo.lower() == titulo.lower():
                libro.prestar()
                return
        print(f"No se encontró el libro titulado '{titulo}'.")

    def devolver_libro(self, titulo):
        for libro in self.catalogo:
            if libro.titulo.lower() == titulo.lower():
                libro.devolver()
                return
        print(f"No se encontró el libro titulado '{titulo}'.")


#! ----------- Menú interactivo ----------- !#

def menu():
    biblio = Biblioteca("Biblioteca Central")

    while True:
        print("\n=== Menú Biblioteca ===")
        print("1. Agregar libro")
        print("2. Mostrar libros")
        print("3. Buscar por autor")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            anio = input("Año de publicación: ")
            libro = Libro(titulo, autor, anio)
            biblio.agregar_libro(libro)

        elif opcion == "2":
            biblio.mostrar_libros()

        elif opcion == "3":
            autor = input("Autor a buscar: ")
            libros = biblio.buscar_libro_por_autor(autor)
            for libro in libros:
                print(libro)

        elif opcion == "4":
            titulo = input("Título del libro a prestar: ")
            biblio.prestar_libro(titulo)

        elif opcion == "5":
            titulo = input("Título del libro a devolver: ")
            biblio.devolver_libro(titulo)

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida, intenta de nuevo.")


# Ejecutar menú si el archivo se corre directamente
if __name__ == "__main__":
    menu()

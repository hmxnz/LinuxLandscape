#! /usr/bin/env python3

class Animal:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie
        self.alimentado = False
    def __str__(self):
        return f"{self.nombre} ({self.especie}) - {'Alimentado :)' if self.alimentado else 'QUE ME QUEDO SIN COMER :('}"


class TiendaAnimales: 
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = []

    def agregar_animal(self, animal):
        self.inventario.append(animal)
        print(f"El animal {animal.nombre} ha sido agregado a la tienda.")

    def mostrar_animales(self):
        if not self.inventario:
            print("No hay animales en la tienda.")
            return
        for animal in self.inventario:
            print(animal)

    def alimentar_animal(self, nombre):
        for animal in self.inventario:
            if animal.nombre.lower() == nombre.lower():
                if not animal.alimentado:
                    animal.alimentado = True
                    print(f"{animal.nombre} ha sido alimentado.")
                else:
                    print(f"{animal.nombre} ya ha sido alimentado.")
                return
        print(f"No se encontró el animal llamado '{nombre}'.")

    def vender_animal(self, nombre):
        for animal in self.inventario:
            if animal.nombre.lower() == nombre.lower():
                self.inventario.remove(animal)
                print(f"{animal.nombre} ha sido vendido.")
                return
        print(f"No se encontró el animal llamado '{nombre}'.")

if __name__ == "__main__":
    tienda = TiendaAnimales("Mi Tienda de Animales")

    # Agregar algunos animales
    perro = Animal("Rex", "Perro")
    gato = Animal("Miau", "Gato")
    loro = Animal("Polly", "Loro")

    tienda.agregar_animal(perro)
    tienda.agregar_animal(gato)
    tienda.agregar_animal(loro)

    # Mostrar animales en la tienda
    tienda.mostrar_animales()

    # Alimentar un animal
    tienda.alimentar_animal("Rex")
    tienda.alimentar_animal("Miau")

    # Mostrar animales nuevamente
    tienda.mostrar_animales()

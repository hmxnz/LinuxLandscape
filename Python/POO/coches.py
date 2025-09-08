#! /usr/bin/env python3
# ------------------------------
# Clase Vehiculo
# ------------------------------
class Vehiculo:
    """
    Clase que representa un vehículo.
    Cada vehículo tiene atributos básicos como marca, modelo, año y estado de disponibilidad.
    """
    def __init__(self, marca, modelo, año):
        self.marca = marca              # Marca del vehículo
        self.modelo = modelo            # Modelo del vehículo
        self.año = año                  # Año del vehículo
        self.disponible = True          # Estado de disponibilidad (True = disponible, False = alquilado)

    def alquilar(self):
        """
        Marca el vehículo como alquilado.
        """
        if self.disponible:
            self.disponible = False
            print(f"Vehículo {self.marca} {self.modelo} alquilado con éxito.")
        else:
            print(f"El vehículo {self.marca} {self.modelo} no está disponible para alquilar.")

    def devolver(self):
        """
        Marca el vehículo como disponible nuevamente.
        """
        if not self.disponible:
            self.disponible = True
            print(f"Vehículo {self.marca} {self.modelo} ha sido devuelto correctamente.")
        else:
            print(f"El vehículo {self.marca} {self.modelo} ya estaba disponible.")

    def __str__(self):
        """
        Representación legible del vehículo.
        """
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"{self.marca} {self.modelo} ({self.año}) - {estado}"


# ------------------------------
# Clase Flota
# ------------------------------
class Flota:
    """
    Clase que representa la flota de vehículos.
    Permite agregar vehículos, listar disponibles, alquilar y devolver vehículos.
    """
    def __init__(self):
        self.vehiculos = []  # Lista que almacena todos los vehículos de la flota

    def agregar_vehiculo(self, vehiculo):
        """
        Agrega un nuevo vehículo a la flota.
        """
        self.vehiculos.append(vehiculo)
        print(f"Vehículo {vehiculo.marca} {vehiculo.modelo} agregado a la flota.")

    def mostrar_disponibles(self):
        """
        Muestra todos los vehículos que están disponibles para alquilar.
        """
        print("\nVehículos disponibles:")
        disponibles = [v for v in self.vehiculos if v.disponible]
        if not disponibles:
            print("No hay vehículos disponibles en este momento.")
        for v in disponibles:
            print(v)

    def alquilar_vehiculo(self, marca, modelo):
        """
        Permite alquilar un vehículo según marca y modelo.
        """
        for v in self.vehiculos:
            if v.marca == marca and v.modelo == modelo:
                v.alquilar()
                return
        print(f"No se encontró un vehículo disponible con marca {marca} y modelo {modelo}.")

    def devolver_vehiculo(self, marca, modelo):
        """
        Permite devolver un vehículo alquilado según marca y modelo.
        """
        for v in self.vehiculos:
            if v.marca == marca and v.modelo == modelo:
                v.devolver()
                return
        print(f"No se encontró un vehículo con marca {marca} y modelo {modelo} en la flota.")


# ------------------------------
# Programa principal
# ------------------------------
def main():
    # Crear la flota
    mi_flota = Flota()

    # Agregar vehículos a la flota
    mi_flota.agregar_vehiculo(Vehiculo("Toyota", "Corolla", 2020))
    mi_flota.agregar_vehiculo(Vehiculo("Honda", "Civic", 2019))
    mi_flota.agregar_vehiculo(Vehiculo("Ford", "Focus", 2021))

    # Mostrar vehículos disponibles
    mi_flota.mostrar_disponibles()

    # Alquilar un vehículo
    mi_flota.alquilar_vehiculo("Toyota", "Corolla")

    # Intentar alquilar un vehículo que ya está alquilado
    mi_flota.alquilar_vehiculo("Toyota", "Corolla")

    # Mostrar vehículos disponibles después del alquiler
    mi_flota.mostrar_disponibles()

    # Devolver un vehículo
    mi_flota.devolver_vehiculo("Toyota", "Corolla")

    # Mostrar vehículos disponibles después de la devolución
    mi_flota.mostrar_disponibles()


# Ejecutar el programa
if __name__ == "__main__":
    main()

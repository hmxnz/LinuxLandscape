#!/usr/bin/env python3
from gestor import GestorNotas
from colorama import Fore, Style, init

# Inicializar colorama (solo necesario en Windows pero lo pongo por si acaso)
init(autoreset=True)

def mostrar_banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
   ____        _   _       _       
  |  _ \ _   _| \ | | ___ | |_ ___ 
  | |_) | | | |  \| |/ _ \| __/ _ \
  |  __/| |_| | |\  | (_) | ||  __/
  |_|    \__, |_| \_|\___/ \__\___|
         |___/                      
    """)
    print(Fore.YELLOW + " 📒 Bienvenido a *PyNotes*, tu gestor de notas avanzado\n")

def mostrar_menu():
    print(Fore.GREEN + "===================================")
    print(Fore.MAGENTA + Style.BRIGHT + "              MENÚ")
    print(Fore.GREEN + "===================================")
    print(Fore.CYAN + "1." + Fore.WHITE + " 📝 Crear nota")
    print(Fore.CYAN + "2." + Fore.WHITE + " 📄 Listar notas")
    print(Fore.CYAN + "3." + Fore.WHITE + " 🔍 Buscar notas")
    print(Fore.CYAN + "4." + Fore.WHITE + " 🗑️  Eliminar nota")
    print(Fore.CYAN + "5." + Fore.WHITE + " 🚪 Salir")
    print(Fore.CYAN + "6." + Fore.WHITE + " ℹ️  Ayuda")
    print(Fore.GREEN + "===================================")

def mostrar_ayuda():
    print(Fore.BLUE + Style.BRIGHT + "\n📖 PANEL DE AYUDA - PyNotes\n")
    print(Fore.WHITE + "PyNotes es un gestor de notas en consola que te permite:")
    print(Fore.CYAN + "1. 📝 Crear nota:" + Fore.WHITE + " Introduce un título y contenido. La nota se guarda automáticamente.")
    print(Fore.CYAN + "2. 📄 Listar notas:" + Fore.WHITE + " Muestra todas las notas almacenadas.")
    print(Fore.CYAN + "3. 🔍 Buscar notas:" + Fore.WHITE + " Encuentra notas que contengan una palabra en el título o contenido.")
    print(Fore.CYAN + "4. 🗑️  Eliminar nota:" + Fore.WHITE + " Elimina una nota indicando su ID.")
    print(Fore.CYAN + "5. 🚪 Salir:" + Fore.WHITE + " Cierra el programa.")
    print(Fore.CYAN + "6. ℹ️  Ayuda:" + Fore.WHITE + " Muestra este panel de ayuda.")
    print(Fore.YELLOW + "\n💾 Nota: Todas las notas se guardan automáticamente en disco (data.pkl) usando Pickle.\n")

def main():
    gestor = GestorNotas()
    mostrar_banner()

    while True:
        mostrar_menu()
        opcion = input(Fore.YELLOW + "👉 Elige una opción: " + Fore.WHITE)

        if opcion == "1":
            titulo = input(Fore.CYAN + "Título: " + Fore.WHITE)
            contenido = input(Fore.CYAN + "Contenido: " + Fore.WHITE)
            gestor.crear_nota(titulo, contenido)

        elif opcion == "2":
            gestor.listar_notas()

        elif opcion == "3":
            criterio = input(Fore.CYAN + "Introduce un texto para buscar: " + Fore.WHITE)
            gestor.buscar_notas(criterio)

        elif opcion == "4":
            try:
                id_nota = int(input(Fore.CYAN + "Introduce el ID de la nota a eliminar: " + Fore.WHITE))
                gestor.eliminar_nota(id_nota)
            except ValueError:
                print(Fore.RED + "❌ ID inválido. Debe ser un número.")

        elif opcion == "5":
            print(Fore.GREEN + "👋 Saliendo de PyNotes. ¡Hasta pronto!")
            break

        elif opcion == "6":
            mostrar_ayuda()

        else:
            print(Fore.RED + "❌ Opción inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()

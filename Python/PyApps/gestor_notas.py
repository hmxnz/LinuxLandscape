#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

# Lista para almacenar las tareas
tareas = []

# Función para actualizar la lista visual de tareas
def actualizar_lista():
    lista_tareas.delete(0, tk.END)
    for tarea in tareas:
        lista_tareas.insert(tk.END, tarea)

# Función para agregar una nueva tarea
def agregar_tarea():
    tarea = entrada_tarea.get()
    if tarea:
        tareas.append(tarea)
        entrada_tarea.delete(0, tk.END)
        actualizar_lista()
    else:
        messagebox.showwarning("Advertencia", "Escribe una tarea antes de agregar.")

# Función para eliminar la tarea seleccionada
def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        indice = seleccion[0]
        tareas.pop(indice)
        actualizar_lista()
    else:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar.")

# Función para actualizar la tarea seleccionada
def actualizar_tarea():
    seleccion = lista_tareas.curselection()
    nueva_tarea = entrada_tarea.get()
    if seleccion and nueva_tarea:
        indice = seleccion[0]
        tareas[indice] = nueva_tarea
        entrada_tarea.delete(0, tk.END)
        actualizar_lista()
    else:
        messagebox.showwarning("Advertencia", "Selecciona una tarea y escribe el nuevo texto.")

# Función para mostrar la tarea seleccionada en la entrada
def mostrar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        entrada_tarea.delete(0, tk.END)
        entrada_tarea.insert(0, tareas[seleccion[0]])

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Tareas Personal")
ventana.geometry("400x400")
ventana.configure(bg="#222831")

# Etiqueta de título
tk.Label(ventana, text="Tus Tareas", bg="#222831", fg="#00ADB5", font=("Arial", 16, "bold")).pack(pady=10)

# Entrada para nueva tarea
entrada_tarea = tk.Entry(ventana, width=30, font=("Arial", 12))
entrada_tarea.pack(pady=5)

# Botones CRUD
frame_botones = tk.Frame(ventana, bg="#222831")
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Agregar", width=10, bg="#00ADB5", fg="#EEEEEE", command=agregar_tarea).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Actualizar", width=10, bg="#F08A5D", fg="#EEEEEE", command=actualizar_tarea).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Eliminar", width=10, bg="#FF2E63", fg="#EEEEEE", command=eliminar_tarea).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="Mostrar", width=10, bg="#393E46", fg="#EEEEEE", command=mostrar_tarea).grid(row=0, column=3, padx=5)

# Lista visual de tareas
lista_tareas = tk.Listbox(ventana, width=40, height=12, font=("Arial", 12), bg="#393E46", fg="#EEEEEE", selectbackground="#00ADB5")
lista_tareas.pack(pady=10)

# Ejecutar la ventana principal
ventana.mainloop()
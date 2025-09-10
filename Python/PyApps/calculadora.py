#!/usr/bin/env python3

import tkinter as tk

# Colores personalizados
COLOR_FONDO = "#222831"
COLOR_PANTALLA = "#393E46"
COLOR_BOTON = "#00ADB5"
COLOR_BOTON_OP = "#F08A5D"
COLOR_TEXTO = "#EEEEEE"

# Función para agregar el texto de los botones a la pantalla
def agregar_texto(valor):
    pantalla.insert(tk.END, valor)

# Función para calcular el resultado de la expresión
def calcular():
    try:
        resultado = eval(pantalla.get())
        pantalla.delete(0, tk.END)
        pantalla.insert(tk.END, str(resultado))
    except Exception:
        pantalla.delete(0, tk.END)
        pantalla.insert(tk.END, "Error")

# Función para limpiar la pantalla
def limpiar():
    pantalla.delete(0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora")
ventana.configure(bg=COLOR_FONDO)

# Crear la pantalla de la calculadora (Entry)
pantalla = tk.Entry(
    ventana, width=25, borderwidth=3, font=('Arial', 14),
    bg=COLOR_PANTALLA, fg=COLOR_TEXTO, justify='right'
)
pantalla.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# Lista de botones (texto y posición)
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

# Crear los botones y asignarles su función y color
for (texto, fila, columna) in botones:
    if texto == '=':
        accion = calcular
        color = COLOR_BOTON_OP
    elif texto in ['/', '*', '-', '+']:
        accion = lambda t=texto: agregar_texto(t)
        color = COLOR_BOTON_OP
    else:
        accion = lambda t=texto: agregar_texto(t)
        color = COLOR_BOTON
    tk.Button(
        ventana, text=texto, width=5, height=2, command=accion,
        bg=color, fg=COLOR_TEXTO, font=('Arial', 12, 'bold')
    ).grid(row=fila, column=columna, padx=2, pady=2)

# Botón para limpiar la pantalla
tk.Button(
    ventana, text='C', width=5, height=2, command=limpiar,
    bg="#FF2E63", fg=COLOR_TEXTO, font=('Arial', 12, 'bold')
).grid(row=5, column=0, columnspan=4, sticky='we', padx=2, pady=2)

# Ejecutar la ventana principal
ventana.mainloop()
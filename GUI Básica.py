"""
Aplicación GUI Básica: Gestor de Productos
-----------------------------------------
Objetivo:
Desarrollar una interfaz gráfica de usuario que permita al usuario agregar
y eliminar productos en una lista, utilizando la librería Tkinter.

Componentes:
- Etiquetas (Label)
- Campo de texto (Entry)
- Botones (Button)
- Lista para mostrar datos (Listbox)

Funcionalidades:
- Agregar productos a la lista mediante un campo de texto.
- Mostrar productos precargados y los que el usuario ingrese.
- Eliminar productos seleccionados o vaciar la lista completa.
"""

import tkinter as tk
from tkinter import messagebox

# ----------------------------
# Función para agregar datos
# ----------------------------
def agregar_dato():
    """Agrega el dato escrito en el campo de texto a la lista."""
    dato = entrada.get().strip()  # Obtener texto sin espacios
    if dato:  # Verifica que no esté vacío
        lista.insert(tk.END, dato)  # Insertar en la lista
        entrada.delete(0, tk.END)   # Limpiar campo de texto
    else:
        messagebox.showinfo("Info", "Debes escribir un producto para agregarlo.")

# ----------------------------
# Función para limpiar la lista
# ----------------------------
def limpiar_datos():
    """Elimina productos seleccionados o toda la lista si no hay selección."""
    seleccion = lista.curselection()
    if seleccion:  # Si el usuario seleccionó algo
        for index in reversed(seleccion):  # Eliminar de atrás hacia adelante
            lista.delete(index)
    else:
        lista.delete(0, tk.END)  # Si no selecciona nada, borra todo

# ----------------------------
# Ventana principal
# ----------------------------
ventana = tk.Tk()
ventana.title("Gestor de Productos - Aplicación GUI Básica")
ventana.geometry("400x400")

# Etiqueta de título
etiqueta = tk.Label(ventana, text="Lista de productos:", font=("Arial", 12))
etiqueta.pack(pady=5)

# Campo de entrada
entrada = tk.Entry(ventana, font=("Arial", 12))
entrada.pack(pady=5)

# Botón para agregar productos
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato, bg="green", fg="white")
boton_agregar.pack(pady=5)

# Lista para mostrar productos
lista = tk.Listbox(ventana, width=40, height=10, font=("Arial", 12))
lista.pack(pady=10)

# Precargar productos iniciales
productos_iniciales = ["Manzana", "Pan", "Leche", "Arroz", "Huevos", "Queso", "Café", "Tomate", "Azúcar"]
for producto in productos_iniciales:
    lista.insert(tk.END, producto)

# Botón para limpiar productos
boton_limpiar = tk.Button(ventana, text="Eliminar seleccionados / todos", command=limpiar_datos, bg="red", fg="white")
boton_limpiar.pack(pady=5)

# Iniciar aplicación
ventana.mainloop()







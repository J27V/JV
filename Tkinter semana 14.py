import tkinter as tk

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Prueba Tkinter")
ventana.geometry("300x200")

# Etiqueta dentro de la ventana
label = tk.Label(ventana, text="¡Hola! Tkinter funciona ✅", font=("Arial", 12))
label.pack(pady=50)

# Mantener ventana abierta
ventana.mainloop()


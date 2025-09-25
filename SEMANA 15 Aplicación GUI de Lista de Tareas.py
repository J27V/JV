import tkinter as tk
from tkinter import messagebox

# =========================
# Clase principal de la aplicación
# =========================
class ListaTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Lista donde se guardarán las tareas y su estado
        self.tareas = []

        # =========================
        # Sección de entrada
        # =========================
        self.entry_tarea = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.entry_tarea.pack(pady=10)
        self.entry_tarea.bind("<Return>", self.agregar_tarea)  # Enter agrega tarea

        # Botones de acción
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=5)

        btn_agregar = tk.Button(frame_botones, text="Añadir Tarea", width=15, command=self.agregar_tarea)
        btn_agregar.grid(row=0, column=0, padx=5)

        btn_completar = tk.Button(frame_botones, text="Marcar como Completada", width=20, command=self.marcar_completada)
        btn_completar.grid(row=0, column=1, padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", width=15, command=self.eliminar_tarea)
        btn_eliminar.grid(row=1, column=0, columnspan=2, pady=5)

        # =========================
        # Listbox para mostrar tareas
        # =========================
        self.listbox = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-Button-1>", self.marcar_completada)  # Doble clic para completar

    # =========================
    # Funciones de la aplicación
    # =========================
    def agregar_tarea(self, event=None):
        """Agrega una nueva tarea a la lista."""
        tarea = self.entry_tarea.get().strip()
        if tarea:
            self.tareas.append({"texto": tarea, "completada": False})
            self.entry_tarea.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Por favor, escribe una tarea antes de añadirla.")

    def marcar_completada(self, event=None):
        """Marca la tarea seleccionada como completada (o la desmarca)."""
        seleccion = self.listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.tareas[indice]["completada"] = not self.tareas[indice]["completada"]
            self.actualizar_lista()
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para marcarla como completada.")

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada."""
        seleccion = self.listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.tareas.pop(indice)
            self.actualizar_lista()
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para eliminarla.")

    def actualizar_lista(self):
        """Actualiza el contenido visual del Listbox."""
        self.listbox.delete(0, tk.END)
        for tarea in self.tareas:
            texto = tarea["texto"]
            if tarea["completada"]:
                texto = "✔ " + texto  # Agregar un check al inicio
            self.listbox.insert(tk.END, texto)


# =========================
# Punto de entrada principal
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = ListaTareasApp(root)
    root.mainloop()

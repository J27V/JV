"""
Agenda Personal con Tkinter
Archivo: agenda_simple.py

Aplicación de agenda personal que permite agregar, ver y eliminar eventos.
No utiliza tkcalendar. La fecha se selecciona con Combobox (día, mes, año).
Los datos se guardan en un archivo JSON.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "eventos.json"


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("750x450")
        self.resizable(False, False)

        self.eventos = []
        self.next_id = 1
        self.cargar_eventos()

        self.crear_interfaz()
        self.actualizar_tabla()

    def crear_interfaz(self):
        # Tabla
        frame_tabla = ttk.Frame(self, padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("fecha", width=120, anchor=tk.CENTER)
        self.tree.column("hora", width=80, anchor=tk.CENTER)
        self.tree.column("descripcion", width=500, anchor=tk.W)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

        # Entrada de datos
        frame_inferior = ttk.Frame(self, padding=10)
        frame_inferior.pack(fill=tk.X)

        # Fecha con Combobox
        ttk.Label(frame_inferior, text="Día:").grid(row=0, column=0, padx=2, pady=5)
        self.combo_dia = ttk.Combobox(frame_inferior, values=[str(i) for i in range(1, 32)], width=5)
        self.combo_dia.current(0)
        self.combo_dia.grid(row=0, column=1, padx=2, pady=5)

        ttk.Label(frame_inferior, text="Mes:").grid(row=0, column=2, padx=2, pady=5)
        self.combo_mes = ttk.Combobox(frame_inferior, values=[str(i) for i in range(1, 13)], width=5)
        self.combo_mes.current(0)
        self.combo_mes.grid(row=0, column=3, padx=2, pady=5)

        ttk.Label(frame_inferior, text="Año:").grid(row=0, column=4, padx=2, pady=5)
        self.combo_anio = ttk.Combobox(frame_inferior, values=[str(i) for i in range(2024, 2035)], width=7)
        self.combo_anio.current(0)
        self.combo_anio.grid(row=0, column=5, padx=2, pady=5)

        # Hora
        ttk.Label(frame_inferior, text="Hora (HH:MM):").grid(row=0, column=6, padx=5, pady=5)
        self.entry_hora = ttk.Entry(frame_inferior, width=10)
        self.entry_hora.insert(0, "09:00")
        self.entry_hora.grid(row=0, column=7, padx=5, pady=5)

        # Descripción
        ttk.Label(frame_inferior, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.entry_desc = tk.Text(frame_inferior, width=60, height=3)
        self.entry_desc.grid(row=1, column=1, columnspan=7, padx=5, pady=5)

        # Botones
        frame_botones = ttk.Frame(frame_inferior)
        frame_botones.grid(row=0, column=8, rowspan=2, padx=10, pady=5, sticky="ns")

        ttk.Button(frame_botones, text="Agregar Evento", command=self.agregar_evento).pack(fill="x", pady=5)
        ttk.Button(frame_botones, text="Eliminar Seleccionado", command=self.eliminar_evento).pack(fill="x", pady=5)
        ttk.Button(frame_botones, text="Salir", command=self.salir).pack(fill="x", pady=5)

    def validar_hora(self, hora):
        try:
            datetime.strptime(hora, "%H:%M")
            return True
        except ValueError:
            return False

    def agregar_evento(self):
        dia = self.combo_dia.get()
        mes = self.combo_mes.get()
        anio = self.combo_anio.get()
        fecha = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"

        hora = self.entry_hora.get().strip()
        descripcion = self.entry_desc.get("1.0", tk.END).strip()

        if not hora or not descripcion:
            messagebox.showwarning("Campos incompletos", "Debe ingresar la hora y la descripción.")
            return

        if not self.validar_hora(hora):
            messagebox.showerror("Hora inválida", "La hora debe estar en formato HH:MM.")
            return

        evento = {"id": self.next_id, "fecha": fecha, "hora": hora, "descripcion": descripcion}
        self.eventos.append(evento)
        self.next_id += 1
        self.guardar_eventos()
        self.actualizar_tabla()

        # Reset
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, "09:00")
        self.entry_desc.delete("1.0", tk.END)

    def eliminar_evento(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showinfo("Eliminar", "Seleccione un evento para eliminar.")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el evento seleccionado?"):
            return

        for item in seleccionado:
            id_evento = int(self.tree.item(item, "iid"))
            self.eventos = [e for e in self.eventos if e["id"] != id_evento]

        self.guardar_eventos()
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        eventos_ordenados = sorted(
            self.eventos,
            key=lambda e: datetime.strptime(e["fecha"] + " " + e["hora"], "%Y-%m-%d %H:%M")
        )
        for ev in eventos_ordenados:
            self.tree.insert("", tk.END, iid=str(ev["id"]), values=(ev["fecha"], ev["hora"], ev["descripcion"]))

    def guardar_eventos(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"next_id": self.next_id, "eventos": self.eventos}, f, ensure_ascii=False, indent=2)

    def cargar_eventos(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.eventos = datos.get("eventos", [])
                self.next_id = datos.get("next_id", 1)

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.guardar_eventos()
            self.destroy()


if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()

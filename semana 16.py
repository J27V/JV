"""
Sistema de Gestión de Inventario con POO, Tkinter y JSON

Autor: ChatGPT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

# ------------------ MODELO ------------------

class Producto:
    def __init__(self, codigo: str, nombre: str, descripcion: str, cantidad: int, precio: float):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio

    def valor_total(self) -> float:
        return self.cantidad * self.precio

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data: dict):
        return Producto(
            data["codigo"],
            data["nombre"],
            data.get("descripcion", ""),
            int(data["cantidad"]),
            float(data["precio"])
        )


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar(self, producto: Producto):
        if any(p.codigo == producto.codigo for p in self.productos):
            raise ValueError(f"El código {producto.codigo} ya existe.")
        self.productos.append(producto)

    def actualizar(self, codigo: str, nuevo: Producto):
        for i, p in enumerate(self.productos):
            if p.codigo == codigo:
                self.productos[i] = nuevo
                return
        raise ValueError(f"No se encontró producto con código {codigo}.")

    def eliminar(self, codigo: str):
        self.productos = [p for p in self.productos if p.codigo != codigo]

    def buscar(self, termino: str, campo="nombre"):
        termino = termino.lower()
        if campo == "nombre":
            return [p for p in self.productos if termino in p.nombre.lower()]
        elif campo == "codigo":
            return [p for p in self.productos if termino in p.codigo.lower()]
        return []

    def guardar(self, archivo="inventario.json"):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.productos], f, indent=4)

    def cargar(self, archivo="inventario.json"):
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.productos = [Producto.from_dict(p) for p in data]


# ------------------ VISTA / CONTROLADOR ------------------

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventario")
        self.inventario = Inventario()
        self.inventario.cargar()

        self._crear_widgets()
        self._refrescar_tabla()

    def _crear_widgets(self):
        # --- Formulario ---
        frm_form = ttk.Frame(self.root)
        frm_form.pack(padx=10, pady=5, fill="x")

        self.entries = {}
        campos = ["Código", "Nombre", "Descripción", "Cantidad", "Precio"]
        for i, campo in enumerate(campos):
            ttk.Label(frm_form, text=campo).grid(row=0, column=i*2, sticky="w")
            entry = ttk.Entry(frm_form)
            entry.grid(row=0, column=i*2+1, padx=5)
            self.entries[campo.lower()] = entry

        # --- Botones ---
        frm_btn = ttk.Frame(self.root)
        frm_btn.pack(padx=10, pady=5, fill="x")

        ttk.Button(frm_btn, text="Agregar", command=self.agregar_producto).pack(side="left")
        ttk.Button(frm_btn, text="Actualizar", command=self.actualizar_producto).pack(side="left", padx=5)
        ttk.Button(frm_btn, text="Eliminar", command=self.eliminar_producto).pack(side="left")
        ttk.Button(frm_btn, text="Guardar", command=self.guardar_inventario).pack(side="right")

        # --- Tabla ---
        self.tree = ttk.Treeview(self.root, columns=("codigo", "nombre", "descripcion", "cantidad", "precio", "valor"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_producto)

    def _refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.inventario.productos:
            self.tree.insert("", "end", values=(p.codigo, p.nombre, p.descripcion, p.cantidad, f"{p.precio:.2f}", f"{p.valor_total():.2f}"))

    def _leer_formulario(self) -> Producto:
        try:
            codigo = self.entries["código"].get().strip()
            nombre = self.entries["nombre"].get().strip()
            descripcion = self.entries["descripción"].get().strip()
            cantidad = int(self.entries["cantidad"].get())
            precio = float(self.entries["precio"].get())
            if not codigo or not nombre:
                raise ValueError("Código y Nombre son obligatorios.")
            return Producto(codigo, nombre, descripcion, cantidad, precio)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    def agregar_producto(self):
        producto = self._leer_formulario()
        if producto:
            try:
                self.inventario.agregar(producto)
                self._refrescar_tabla()
                messagebox.showinfo("Éxito", "Producto agregado.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def actualizar_producto(self):
        producto = self._leer_formulario()
        if producto:
            try:
                self.inventario.actualizar(producto.codigo, producto)
                self._refrescar_tabla()
                messagebox.showinfo("Éxito", "Producto actualizado.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def eliminar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
            return
        codigo = self.tree.item(sel[0])["values"][0]
        self.inventario.eliminar(codigo)
        self._refrescar_tabla()
        messagebox.showinfo("Éxito", "Producto eliminado.")

    def guardar_inventario(self):
        self.inventario.guardar()
        messagebox.showinfo("Éxito", "Inventario guardado en archivo.")

    def seleccionar_producto(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        valores = self.tree.item(sel[0])["values"]
        self.entries["código"].delete(0, "end"); self.entries["código"].insert(0, valores[0])
        self.entries["nombre"].delete(0, "end"); self.entries["nombre"].insert(0, valores[1])
        self.entries["descripción"].delete(0, "end"); self.entries["descripción"].insert(0, valores[2])
        self.entries["cantidad"].delete(0, "end"); self.entries["cantidad"].insert(0, valores[3])
        self.entries["precio"].delete(0, "end"); self.entries["precio"].insert(0, valores[4])


# ------------------ MAIN ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()

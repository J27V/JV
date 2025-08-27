#!/usr/bin/env python3
"""
inventory_system.py

Sistema avanzado de gestión de inventario (único archivo).
- Clases: Producto, Inventario
- Persistencia en archivo JSON
- Uso de colecciones: dict, list, set, tuple
- Menú interactivo por consola
"""

import json
import uuid
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Tuple, Optional, Set

INVENTORY_FILENAME = "inventario.json"


@dataclass
class Producto:
    """Clase que representa un producto en el inventario."""
    id: str
    nombre: str
    cantidad: int
    precio: float

    def to_dict(self) -> dict:
        """Serialización a diccionario (útil para JSON)."""
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Producto":
        """Construye un Producto a partir de un diccionario."""
        return Producto(
            id=d["id"],
            nombre=d["nombre"],
            cantidad=int(d["cantidad"]),
            precio=float(d["precio"])
        )

    def resumen_tuple(self) -> Tuple[str, str, int, float]:
        """Devuelve un resumen inmutable (tupla) del producto."""
        return (self.id, self.nombre, self.cantidad, self.precio)


class Inventario:
    """
    Clase Inventario:
    - Usa un diccionario para mapear product_id -> Producto (búsqueda O(1) por ID).
    - Mantiene un set de nombres (lowercase) para búsquedas rápidas por nombre sin duplicados.
    """
    def __init__(self):
        self._productos: Dict[str, Producto] = {}
        # Set para nombres en minúsculas (ayuda a chequear existencia rápida y búsquedas)
        self._nombres_set: Set[str] = set()

    # ---------- Operaciones CRUD ----------
    def generar_id_unico(self) -> str:
        """Genera un UUID corto (sin guiones)."""
        return uuid.uuid4().hex[:12]

    def añadir_producto(self, nombre: str, cantidad: int, precio: float, producto_id: Optional[str] = None) -> Producto:
        """Añade un nuevo producto. Retorna el Producto creado.
        Si se pasa producto_id intenta usarlo (pero debe ser único)."""
        if producto_id is None:
            producto_id = self.generar_id_unico()
        if producto_id in self._productos:
            raise ValueError(f"ID '{producto_id}' ya existe en el inventario.")

        nuevo = Producto(id=producto_id, nombre=nombre.strip(), cantidad=int(cantidad), precio=float(precio))
        self._productos[nuevo.id] = nuevo
        self._nombres_set.add(nuevo.nombre.lower())
        return nuevo

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto por ID. Retorna True si se eliminó, False si no existía."""
        if producto_id in self._productos:
            nombre = self._productos[producto_id].nombre.lower()
            del self._productos[producto_id]
            # actualizar set de nombres (recalcular para mayor seguridad)
            self._recalcular_nombres_set()
            return True
        return False

    def actualizar_cantidad(self, producto_id: str, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto. Retorna True si tuvo éxito."""
        p = self._productos.get(producto_id)
        if not p:
            return False
        p.cantidad = int(nueva_cantidad)
        return True

    def actualizar_precio(self, producto_id: str, nuevo_precio: float) -> bool:
        """Actualiza el precio de un producto. Retorna True si tuvo éxito."""
        p = self._productos.get(producto_id)
        if not p:
            return False
        p.precio = float(nuevo_precio)
        return True

    # ---------- Búsquedas y listados ----------
    def buscar_por_nombre(self, nombre_parcial: str) -> List[Producto]:
        """Busca productos cuyo nombre contiene la cadena (case-insensitive)."""
        nombre_parcial = nombre_parcial.strip().lower()
        resultados: List[Producto] = []
        # recorremos dict (O(n)) pero es razonable; el set ayuda a testear existencia exacta
        for p in self._productos.values():
            if nombre_parcial in p.nombre.lower():
                resultados.append(p)
        return resultados

    def obtener_todos(self) -> List[Producto]:
        """Retorna lista con todos los productos (orden no garantizado)."""
        return list(self._productos.values())

    def obtener_resumen_todos(self) -> List[Tuple[str, str, int, float]]:
        """Retorna lista de tuplas resumen (id, nombre, cantidad, precio)."""
        return [p.resumen_tuple() for p in self._productos.values()]

    def conteo_total_items(self) -> int:
        """Cuenta total de ítems (suma de cantidades)."""
        return sum(p.cantidad for p in self._productos.values())

    # ---------- Persistencia en archivo ----------
    def guardar_en_archivo(self, filename: str = INVENTORY_FILENAME) -> None:
        """Serializa el inventario a JSON y escribe en archivo."""
        serializable = {pid: prod.to_dict() for pid, prod in self._productos.items()}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

    def cargar_desde_archivo(self, filename: str = INVENTORY_FILENAME) -> None:
        """Carga inventario desde archivo JSON. Si no existe, mantiene inventario vacío."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._productos = {pid: Producto.from_dict(prod_dict) for pid, prod_dict in data.items()}
            self._recalcular_nombres_set()
        except FileNotFoundError:
            # Archivo no existe: dejamos inventario vacío
            self._productos = {}
            self._nombres_set = set()
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al leer el archivo JSON: {e}")

    def _recalcular_nombres_set(self) -> None:
        """Recalcula el set de nombres a partir del dict de productos."""
        self._nombres_set = {p.nombre.lower() for p in self._productos.values()}

    # ---------- Utilidades ----------
    def existe_nombre(self, nombre: str) -> bool:
        """Chequea (rápido) si existe un nombre de producto (case-insensitive)."""
        return nombre.strip().lower() in self._nombres_set

    def exportar_csv(self, filename: str) -> None:
        """Exporta el inventario a CSV simple (UTF-8)."""
        import csv
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nombre", "cantidad", "precio"])
            for p in self._productos.values():
                writer.writerow([p.id, p.nombre, p.cantidad, p.precio])


# ---------- Interfaz de consola ----------
def mostrar_menu():
    print("\n--- Menú Inventario ---")
    print("1) Añadir producto")
    print("2) Eliminar producto por ID")
    print("3) Actualizar cantidad")
    print("4) Actualizar precio")
    print("5) Buscar por nombre")
    print("6) Mostrar todos los productos")
    print("7) Guardar inventario en archivo")
    print("8) Cargar inventario desde archivo")
    print("9) Exportar CSV")
    print("0) Salir")


def pedir_input(prompt: str, tipo: type = str, defecto=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and defecto is not None:
            return defecto
        try:
            return tipo(raw)
        except Exception:
            print(f"Entrada inválida. Se esperaba {tipo.__name__}.")


def main():
    inv = Inventario()
    # Intentamos cargar inventario al iniciar para persistencia entre ejecuciones
    try:
        inv.cargar_desde_archivo()
        print(f"Inventario cargado desde '{INVENTORY_FILENAME}'. Productos: {len(inv.obtener_todos())}")
    except Exception as e:
        print(f"No se pudo cargar inventario: {e}")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            if nombre == "":
                print("El nombre no puede estar vacío.")
                continue
            cantidad = pedir_input("Cantidad: ", int, defecto=0)
            precio = pedir_input("Precio: ", float, defecto=0.0)
            if inv.existe_nombre(nombre):
                print("Atención: ya existe un producto con ese nombre (case-insensitive). Se añadirá otro con distinto ID.")
            p = inv.añadir_producto(nombre=nombre, cantidad=cantidad, precio=precio)
            print(f"Producto añadido: {p.resumen_tuple()}")

        elif opcion == "2":
            pid = input("ID del producto a eliminar: ").strip()
            if inv.eliminar_producto(pid):
                print("Producto eliminado.")
            else:
                print("No se encontró producto con ese ID.")

        elif opcion == "3":
            pid = input("ID del producto a actualizar cantidad: ").strip()
            if pid not in inv._productos:
                print("ID no encontrado.")
                continue
            nueva_cant = pedir_input("Nueva cantidad: ", int)
            inv.actualizar_cantidad(pid, nueva_cant)
            print("Cantidad actualizada.")

        elif opcion == "4":
            pid = input("ID del producto a actualizar precio: ").strip()
            if pid not in inv._productos:
                print("ID no encontrado.")
                continue
            nuevo_precio = pedir_input("Nuevo precio: ", float)
            inv.actualizar_precio(pid, nuevo_precio)
            print("Precio actualizado.")

        elif opcion == "5":
            termino = input("Buscar por nombre (parcial): ").strip()
            resultados = inv.buscar_por_nombre(termino)
            if not resultados:
                print("No se encontraron productos.")
            else:
                print(f"Se encontraron {len(resultados)} producto(s):")
                for p in resultados:
                    print(f"- ID: {p.id} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: {p.precio}")

        elif opcion == "6":
            todos = inv.obtener_todos()
            if not todos:
                print("Inventario vacío.")
            else:
                print(f"Todos los productos ({len(todos)}):")
                for p in todos:
                    print(f"- ID: {p.id} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: {p.precio}")
                print(f"Total ítems (suma de cantidades): {inv.conteo_total_items()}")

        elif opcion == "7":
            inv.guardar_en_archivo()
            print(f"Inventario guardado en '{INVENTORY_FILENAME}'.")

        elif opcion == "8":
            inv.cargar_desde_archivo()
            print(f"Inventario recargado desde '{INVENTORY_FILENAME}'. Productos: {len(inv.obtener_todos())}")

        elif opcion == "9":
            fname = input("Nombre archivo CSV (ej: inventario.csv): ").strip()
            if not fname:
                print("Nombre inválido.")
            else:
                inv.exportar_csv(fname)
                print(f"Exportado a '{fname}'.")

        elif opcion == "0":
            # Guardado automático antes de salir
            try:
                inv.guardar_en_archivo()
                print(f"Inventario guardado en '{INVENTORY_FILENAME}'. Saliendo...")
            except Exception as e:
                print(f"No se pudo guardar al salir: {e}")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()

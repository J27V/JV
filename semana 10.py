"""
Sistema de Gestión de Inventarios Mejorado
Archivo único y simplificado para ejecución directa
"""

import os

# --------------------------
# Clase Producto
# --------------------------
class Producto:
    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float):
        self.id = str(id_producto)
        self.nombre = str(nombre)
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def to_line(self) -> str:
        return f"{self.id}|{self.nombre}|{self.cantidad}|{self.precio}\n"

    @staticmethod
    def from_line(line: str):
        parts = line.strip().split("|")
        if len(parts) != 4:
            raise ValueError("Formato de línea inválido")
        id_producto, nombre, cantidad_str, precio_str = parts
        return Producto(id_producto, nombre, int(cantidad_str), float(precio_str))

    def __repr__(self):
        return f"{self.id} | {self.nombre} | Cant: {self.cantidad} | Precio: {self.precio}"

# --------------------------
# Clase Inventario
# --------------------------
class Inventario:
    def __init__(self, ruta="inventario.txt"):
        self.ruta = ruta
        self.productos = {}
        self._cargar()

    def _cargar(self):
        if not os.path.exists(self.ruta):
            return
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            p = Producto.from_line(line)
                            self.productos[p.id] = p
                        except Exception:
                            print(f"[ADVERTENCIA] Línea ignorada: {line.strip()}")
        except Exception as e:
            print(f"[ERROR] No se pudo cargar archivo: {e}")

    def _guardar(self):
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                for p in self.productos.values():
                    f.write(p.to_line())
        except Exception as e:
            print(f"[ERROR] No se pudo guardar: {e}")

    def añadir(self, p: Producto):
        if p.id in self.productos:
            print("[INFO] Producto ya existe")
            return False
        self.productos[p.id] = p
        self._guardar()
        print("[OK] Producto añadido")
        return True

    def actualizar(self, idp, nombre=None, cantidad=None, precio=None):
        if idp not in self.productos:
            print("[INFO] Producto no encontrado")
            return False
        p = self.productos[idp]
        if nombre: p.nombre = nombre
        if cantidad is not None: p.cantidad = cantidad
        if precio is not None: p.precio = precio
        self._guardar()
        print("[OK] Producto actualizado")
        return True

    def eliminar(self, idp):
        if idp not in self.productos:
            print("[INFO] Producto no encontrado")
            return False
        del self.productos[idp]
        self._guardar()
        print("[OK] Producto eliminado")
        return True

    def buscar(self, idp):
        return self.productos.get(idp)

    def listar(self):
        return list(self.productos.values())

# --------------------------
# Menú
# --------------------------
def menu():
    print("\n--- INVENTARIO ---")
    print("1. Listar")
    print("2. Añadir")
    print("3. Actualizar")
    print("4. Eliminar")
    print("5. Buscar")
    print("0. Salir")

def main():
    inv = Inventario()
    while True:
        menu()
        op = input("Opción: ").strip()
        if op == "1":
            prods = inv.listar()
            if not prods:
                print("Inventario vacío")
            for p in prods:
                print(p)
        elif op == "2":
            idp = input("ID: ")
            nombre = input("Nombre: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
            except:
                print("[ERROR] Valores inválidos")
                continue
            inv.añadir(Producto(idp, nombre, cantidad, precio))
        elif op == "3":
            idp = input("ID a actualizar: ")
            p = inv.buscar(idp)
            if not p:
                print("No encontrado")
                continue
            nombre = input(f"Nuevo nombre ({p.nombre}): ") or p.nombre
            try:
                cantidad = input(f"Nueva cantidad ({p.cantidad}): ")
                cantidad = int(cantidad) if cantidad else p.cantidad
                precio = input(f"Nuevo precio ({p.precio}): ")
                precio = float(precio) if precio else p.precio
            except:
                print("[ERROR] Valores inválidos")
                continue
            inv.actualizar(idp, nombre, cantidad, precio)
        elif op == "4":
            idp = input("ID a eliminar: ")
            inv.eliminar(idp)
        elif op == "5":
            idp = input("ID a buscar: ")
            p = inv.buscar(idp)
            print(p if p else "No encontrado")
        elif op == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

# --------------------------
# Ejecutar
# --------------------------
if __name__ == "__main__":
    main()




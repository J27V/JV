# ==============================
# Sistema de Gestión de Inventario
# Todo en un solo archivo
# ==============================

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"


# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("❌ Error: El ID ya existe.")
                return False
        self.productos.append(producto)
        print("✅ Producto agregado.")
        return True

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("✅ Producto eliminado.")
                return True
        print("❌ Producto no encontrado.")
        return False

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("✅ Producto actualizado.")
                return True
        print("❌ Producto no encontrado.")
        return False

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_todos(self):
        if not self.productos:
            print("📦 El inventario está vacío.")
        else:
            for p in self.productos:
                print(p)


# Menú principal
def menu():
    inventario = Inventario()

    # Productos precargados
    inventario.agregar_producto(Producto("P001", "Arroz", 50, 1.20))
    inventario.agregar_producto(Producto("P002", "Azúcar", 30, 0.95))
    inventario.agregar_producto(Producto("P003", "Aceite", 20, 3.50))
    inventario.agregar_producto(Producto("P004", "Leche", 40, 0.80))
    inventario.agregar_producto(Producto("P005", "Huevos", 60, 0.10))

    while True:
        print("\n===== 📋 MENÚ DE INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = input("Ingrese ID: ")
                nombre = input("Ingrese nombre: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                inventario.agregar_producto(Producto(id_producto, nombre, cantidad, precio))
            except ValueError:
                print("⚠️ Error: cantidad y precio deben ser numéricos.")

        elif opcion == "2":
            id_producto = input("ID a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("ID a actualizar: ")
            try:
                cantidad = input("Nueva cantidad (enter para omitir): ")
                precio = input("Nuevo precio (enter para omitir): ")

                cantidad = int(cantidad) if cantidad.strip() != "" else None
                precio = float(precio) if precio.strip() != "" else None

                inventario.actualizar_producto(id_producto, cantidad, precio)
            except ValueError:
                print("⚠️ Error: cantidad y precio deben ser numéricos.")

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print("🔎 Encontrados:")
                for p in resultados:
                    print(p)
            else:
                print("❌ No se encontró.")

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("👋 Saliendo...")
            break
        else:
            print("⚠️ Opción no válida.")


if __name__ == "__main__":
    menu()



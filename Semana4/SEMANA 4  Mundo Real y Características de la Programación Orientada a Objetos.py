# Clase Producto
class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def mostrar_info(self):
        return f"{self.nombre} - ${self.precio:.2f}"


# Clase Cliente
class Cliente:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo


# Clase Carrito de Compras
class Carrito:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)
        print(f"{producto.nombre} agregado al carrito.")

    def mostrar_carrito(self):
        print(f"\nCarrito de {self.cliente.nombre}:")
        total = 0
        for producto in self.productos:
            print(f"- {producto.mostrar_info()}")
            total += producto.precio
        print(f"Total: ${total:.2f}")


# Prueba del sistema
if __name__ == "__main__":
    # Crear productos
    prod1 = Producto("P001", "Reloj inalámbrico", 55.50)
    prod2 = Producto("P002", "Teclado mecánico", 25.90)
    prod3 = Producto("P003", "Audífonos ", 20.00)

    # Crear cliente
    cliente1 = Cliente("María Torres", "maria@email.com")

    # Crear carrito para ese cliente
    carrito1 = Carrito(cliente1)

    # Agregar productos al carrito
    carrito1.agregar_producto(prod1)
    carrito1.agregar_producto(prod2)
    carrito1.agregar_producto(prod3)

    # Mostrar resumen del carrito
    carrito1.mostrar_carrito()

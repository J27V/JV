# usuario.py

class Usuario:
    def __init__(self, nombre, correo):
        """
        Constructor de la clase.
        Se ejecuta automáticamente al crear un objeto.
        Inicializa el nombre y el correo del usuario.
        """
        self.nombre = nombre
        self.correo = correo
        print(f"Usuario '{self.nombre}' ha iniciado sesión con el correo '{self.correo}'.")

    def mostrar_info(self):
        """Muestra la información del usuario."""
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")

    def __del__(self):
        """
        Destructor de la clase.
        Se ejecuta automáticamente al eliminar el objeto.
        Simula el cierre de sesión del usuario.
        """
        print(f"Usuario '{self.nombre}' ha cerrado sesión. Recursos liberados.")


# Bloque principal de prueba
if __name__ == "__main__":
    usuario1 = Usuario("Jakelyn veloz ", "jakelyn.veloz@mail.com")
    usuario1.mostrar_info()

    print("Eliminando el objeto usuario1...")
    del usuario1  # Se activa el destructor

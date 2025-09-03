# ==============================
# Sistema de Gestión de Biblioteca Digital
# ==============================

# Clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Usamos una tupla (titulo, autor) como inmutable
        self.info = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"[{self.isbn}] {self.info[0]} - {self.info[1]} ({self.categoria})"


# Clase Usuario
class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []  # Lista de libros prestados

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.user_id})"


# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.libros = {}        # Diccionario {ISBN: Libro}
        self.usuarios = {}      # Diccionario {ID: Usuario}
        self.ids_usuarios = set()  # Conjunto para IDs únicos

    # ----- Gestión de libros -----
    def agregar_libro(self, libro):
        if libro.isbn in self.libros:
            print(f"❌ El libro con ISBN {libro.isbn} ya existe.")
        else:
            self.libros[libro.isbn] = libro
            print(f"✅ Libro agregado: {libro}")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            eliminado = self.libros.pop(isbn)
            print(f"🗑️ Libro eliminado: {eliminado}")
        else:
            print(f"❌ No se encontró el libro con ISBN {isbn}")

    # ----- Gestión de usuarios -----
    def registrar_usuario(self, usuario):
        if usuario.user_id in self.ids_usuarios:
            print(f"❌ El usuario con ID {usuario.user_id} ya está registrado.")
        else:
            self.usuarios[usuario.user_id] = usuario
            self.ids_usuarios.add(usuario.user_id)
            print(f"✅ Usuario registrado: {usuario}")

    def dar_baja_usuario(self, user_id):
        if user_id in self.usuarios:
            eliminado = self.usuarios.pop(user_id)
            self.ids_usuarios.remove(user_id)
            print(f"🗑️ Usuario dado de baja: {eliminado}")
        else:
            print(f"❌ No se encontró el usuario con ID {user_id}")

    # ----- Préstamos -----
    def prestar_libro(self, user_id, isbn):
        if user_id not in self.usuarios:
            print("❌ Usuario no registrado.")
            return
        if isbn not in self.libros:
            print("❌ Libro no disponible.")
            return

        usuario = self.usuarios[user_id]
        libro = self.libros.pop(isbn)  # Se quita del catálogo disponible
        usuario.libros_prestados.append(libro)
        print(f"📚 Libro prestado: {libro} a {usuario.nombre}")

    def devolver_libro(self, user_id, isbn):
        if user_id not in self.usuarios:
            print("❌ Usuario no registrado.")
            return

        usuario = self.usuarios[user_id]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros[isbn] = libro
                print(f"🔄 Libro devuelto: {libro} por {usuario.nombre}")
                return
        print(f"❌ El usuario {usuario.nombre} no tiene prestado el libro con ISBN {isbn}")

    # ----- Búsqueda -----
    def buscar_libro(self, criterio, valor):
        resultados = []
        for libro in self.libros.values():
            if (criterio == "titulo" and valor.lower() in libro.info[0].lower()) or \
               (criterio == "autor" and valor.lower() in libro.info[1].lower()) or \
               (criterio == "categoria" and valor.lower() in libro.categoria.lower()):
                resultados.append(libro)

        if resultados:
            print(f"🔎 Resultados de búsqueda por {criterio}='{valor}':")
            for libro in resultados:
                print(f"   - {libro}")
        else:
            print(f"❌ No se encontraron libros para {criterio}='{valor}'")

    # ----- Listar libros prestados -----
    def listar_libros_prestados(self, user_id):
        if user_id not in self.usuarios:
            print("❌ Usuario no registrado.")
            return
        usuario = self.usuarios[user_id]
        if usuario.libros_prestados:
            print(f"📖 Libros prestados a {usuario.nombre}:")
            for libro in usuario.libros_prestados:
                print(f"   - {libro}")
        else:
            print(f"ℹ️ El usuario {usuario.nombre} no tiene libros prestados.")


# ==============================
# PRUEBAS DEL SISTEMA
# ==============================
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca()

    # Agregar libros
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "ISBN001")
    libro2 = Libro("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", "ISBN002")
    libro3 = Libro("Python para Todos", "Raúl González", "Programación", "ISBN003")

    biblio.agregar_libro(libro1)
    biblio.agregar_libro(libro2)
    biblio.agregar_libro(libro3)

    # Registrar usuarios
    usuario1 = Usuario("Ana Pérez", "U001")
    usuario2 = Usuario("Carlos Ruiz", "U002")

    biblio.registrar_usuario(usuario1)
    biblio.registrar_usuario(usuario2)

    # Prestar libros
    biblio.prestar_libro("U001", "ISBN001")
    biblio.prestar_libro("U002", "ISBN002")

    # Listar libros prestados
    biblio.listar_libros_prestados("U001")
    biblio.listar_libros_prestados("U002")

    # Buscar libros
    biblio.buscar_libro("titulo", "Python")
    biblio.buscar_libro("autor", "Cervantes")

    # Devolver libros
    biblio.devolver_libro("U001", "ISBN001")

    # Dar de baja usuario
    biblio.dar_baja_usuario("U002")

    # Quitar libro
    biblio.quitar_libro("ISBN003")

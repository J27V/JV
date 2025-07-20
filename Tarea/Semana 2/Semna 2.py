# abstraccion/electrodomestico.py

from abc import ABC, abstractmethod

class Electrodomestico(ABC):
    @abstractmethod
    def encender(self):
        pass

class Televisor(Electrodomestico):
    def encender(self):
        print("El televisor se está encendiendo...")

class Lavadora(Electrodomestico):
    def encender(self):
        print("La lavadora está iniciando el ciclo de lavado...")

# Uso
tv = Televisor()
lavadora = Lavadora()
tv.encender()
lavadora.encender()
# encapsulacion/estudiante.py

class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre
        self.__calificacion = 0  # atributo privado

    def asignar_calificacion(self, nota):
        if 0 <= nota <= 100:
            self.__calificacion = nota
        else:
            print("Nota inválida.")

    def obtener_calificacion(self):
        return self.__calificacion

# Uso
e = Estudiante("Ana")
e.asignar_calificacion(95)
print(f"Calificación de {e.nombre}: {e.obtener_calificacion()}")
# herencia/empleado.py

class Empleado:
    def __init__(self, nombre):
        self.nombre = nombre

    def trabajar(self):
        print(f"{self.nombre} está trabajando.")

class Gerente(Empleado):
    def trabajar(self):
        print(f"{self.nombre} está gestionando el equipo.")

class Desarrollador(Empleado):
    def trabajar(self):
        print(f"{self.nombre} está escribiendo código.")

# Uso
g = Gerente("Laura")
d = Desarrollador("Carlos")
g.trabajar()
d.trabajar()
# polimorfismo/instrumentos.py

class Instrumento:
    def tocar(self):
        print("Este instrumento hace un sonido.")

class Guitarra(Instrumento):
    def tocar(self):
        print("La guitarra está sonando: ♫♪")

class Tambor(Instrumento):
    def tocar(self):
        print("El tambor está sonando: BUM BUM")

def hacer_musica(instrumento):
    instrumento.tocar()

# Uso
guitarra = Guitarra()
tambor = Tambor()

for inst in [guitarra, tambor]:
    hacer_musica(inst)

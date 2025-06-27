# Programa: Ejemplo de Programación Orientada a Objetos
# Tema: Herencia, Encapsulación y Polimorfismo
# Autor: [Tu Nombre]
# Fecha: [Fecha]
# Descripción: Este programa modela vehículos utilizando clases y POO

# Clase base
class Vehiculo:
    def __init__(self, marca, modelo):
        # Atributos públicos
        self.marca = marca
        self.modelo = modelo
        # Atributo privado (encapsulado)
        self.__encendido = False

    # Método para encender el vehículo
    def encender(self):
        self.__encendido = True
        print(f"{self.marca} {self.modelo} está encendido.")

    # Método para apagar el vehículo
    def apagar(self):
        self.__encendido = False
        print(f"{self.marca} {self.modelo} está apagado.")

    # Método para mostrar estado de encendido (acceso al atributo privado)
    def estado_encendido(self):
        if self.__encendido:
            print(f"{self.marca} {self.modelo} está actualmente encendido.")
        else:
            print(f"{self.marca} {self.modelo} está actualmente apagado.")

    # Método que será sobrescrito (polimorfismo)
    def conducir(self):
        print("El vehículo está en movimiento.")

# Clase derivada que hereda de Vehiculo
class Moto(Vehiculo):
    def __init__(self, marca, modelo, cilindrada):
        # Llamar al constructor de la clase base
        super().__init__(marca, modelo)
        # Atributo específico de la moto
        self.cilindrada = cilindrada

    # Sobrescritura del método conducir (polimorfismo)
    def conducir(self):
        print(f"La moto {self.marca} {self.modelo} de {self.cilindrada}cc está conduciendo sobre dos ruedas.")

# Otra clase derivada
class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        # Constructor de la clase base
        super().__init__(marca, modelo)
        self.puertas = puertas

    # Sobrescritura del método conducir (polimorfismo)
    def conducir(self):
        print(f"El auto {self.marca} {self.modelo} con {self.puertas} puertas está conduciendo sobre cuatro ruedas.")

# Crear instancias de las clases
vehiculo1 = Vehiculo("Generic", "X100")
moto1 = Moto("Daytona", "2025", 300)
auto1 = Auto("Mazda", "CX-5", 4)

# Uso de métodos
vehiculo1.encender()
vehiculo1.estado_encendido()
vehiculo1.conducir()
vehiculo1.apagar()
vehiculo1.estado_encendido()

print("\n--- Ejemplo de polimorfismo ---")
moto1.encender()
moto1.conducir()  # método sobrescrito

auto1.encender()
auto1.conducir()  # método sobrescrito


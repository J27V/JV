def obtener_temperaturas_diarias():
    """
    Retorna una lista predefinida de temperaturas diarias para la semana.
    Puedes modificar estos valores según sea necesario.
    """
    # Define aquí las temperaturas para cada día de la semana.
    # Por ejemplo: Lunes, martes, miércoles, jueves, viernes, sábado, domingo
    temperaturas = [20.5, 21.0, 19.8, 22.1, 20.0, 23.5, 21.2]

    print("Usando las siguientes temperaturas predefinidas para la semana:")
    print(temperaturas)
    return temperaturas

def calcular_promedio_semanal(lista_temperaturas):
    """
    Calcula el promedio de una lista de temperaturas.
    Retorna el promedio calculado.
    """
    if not lista_temperaturas:
        # Si la lista está vacía, el promedio es 0 para evitar errores de división.
        return 0
    suma_temperaturas = sum(lista_temperaturas)
    promedio = suma_temperaturas / len(lista_temperaturas)
    return promedio

def main():
    """
    Función principal que organiza la ejecución del programa.
    """
    print("--- Programa de Cálculo de Temperatura Semanal (Versión con Datos Fijos) ---")

    # Paso 1: Obtener las temperaturas diarias.
    # En esta versión, la función 'obtener_temperaturas_diarias' ya devuelve los valores definidos.
    temperaturas_semana = obtener_temperaturas_diarias()

    # Paso 2: Calcular el promedio de esas temperaturas.
    promedio = calcular_promedio_semanal(temperaturas_semana)

    # Paso 3: Mostrar los resultados al usuario.
    print(f"\nLas temperaturas utilizadas son: {temperaturas_semana}")
    print(f"El promedio de la temperatura semanal es: {promedio:.2f}°C") # Formateamos a dos decimales

if __name__ == "__main__":
    # Esta línea asegura que la función 'main()' se ejecute solo cuando el script es el programa principal.
    main()
import statistics # Necesario para calcular el promedio

class DiaClima:
    """
    Representa la información del clima para un día específico.
    Encapsula el nombre del día y su temperatura.
    """
    def __init__(self, nombre_dia: str, temperatura: float = 0.0):
        """
        Constructor de la clase DiaClima.
        """
        self.__nombre_dia = nombre_dia  # Atributo privado
        self.__temperatura = temperatura # Atributo privado

    def get_nombre_dia(self) -> str:
        """Retorna el nombre del día."""
        return self.__nombre_dia

    def get_temperatura(self) -> float:
        """Retorna la temperatura del día."""
        return self.__temperatura

    def set_temperatura(self, temperatura: float):
        """
        Establece la temperatura para el día con validación básica.
        """
        if isinstance(temperatura, (int, float)):
            self.__temperatura = float(temperatura)
        else:
            raise ValueError("La temperatura debe ser un número.")

    def __str__(self):
        """
        Representación en cadena del objeto, útil para imprimir.
        """
        return f"{self.__nombre_dia}: {self.__temperatura:.1f}°C"

# --- Ejemplo de Herencia (Opcional) ---
# Esta clase no se usa directamente en el ejemplo, pero muestra cómo podrías extender DiaClima.
class DiaSoleado(DiaClima):
    """
    Extiende DiaClima para incluir horas de sol.
    """
    def __init__(self, nombre_dia: str, temperatura: float, horas_sol: float):
        super().__init__(nombre_dia, temperatura)
        self.__horas_sol = horas_sol

    def get_horas_sol(self) -> float:
        return self.__horas_sol

    def __str__(self):
        return f"{super().__str__()} (Horas de Sol: {self.__horas_sol})"


class SemanaClima:
    """
    Gestiona una colección de objetos DiaClima para una semana.
    """
    def __init__(self):
        """
        Inicializa una lista vacía para los objetos DiaClima.
        """
        self.__dias_clima = [] # Lista privada para almacenar los días

    def agregar_dia_clima(self, dia_clima: DiaClima):
        """
        Añade un objeto DiaClima a la semana.
        """
        if isinstance(dia_clima, DiaClima):
            self.__dias_clima.append(dia_clima)
        else:
            print("Error: Solo se pueden agregar objetos de tipo DiaClima.")

    def cargar_temperaturas_predefinidas(self):
        """
        Carga temperaturas predefinidas en la semana.
        """
        # Puedes cambiar estos valores si lo deseas
        temperaturas_predefinidas = [22.5, 23.0, 21.8, 24.1, 20.0, 25.3, 22.9]
        dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        print("Cargando temperaturas predefinidas para la semana:")
        for i, nombre_dia in enumerate(dias_nombres):
            temperatura = temperaturas_predefinidas[i]
            dia = DiaClima(nombre_dia)
            dia.set_temperatura(temperatura)
            self.agregar_dia_clima(dia)
            print(f"- {dia}") # Muestra el día y su temperatura a medida que se carga

    def calcular_promedio_semanal(self) -> float:
        """
        Calcula el promedio de las temperaturas de la semana.
        """
        if not self.__dias_clima:
            return 0.0

        temperaturas = [dia.get_temperatura() for dia in self.__dias_clima]
        return statistics.mean(temperaturas)

    def mostrar_informacion_semanal(self):
        """
        Muestra la información de cada día de la semana.
        """
        if not self.__dias_clima:
            print("No hay datos de clima para la semana.")
            return

        print("\n--- Resumen de Temperaturas Diarias Cargadas ---")
        for dia in self.__dias_clima:
            print(dia) # Esto usa el método __str__ de DiaClima

# --- Función Principal del Programa ---
def main():
    """
    Orquesta la ejecución del programa.
    """
    print("--- Programa de Clima Semanal (POO con Datos Fijos) ---")

    mi_semana = SemanaClima()

    # Cargar las temperaturas predefinidas
    mi_semana.cargar_temperaturas_predefinidas()

    # El resumen de temperaturas se imprime durante la carga, pero puedes llamarlo de nuevo si quieres
    # mi_semana.mostrar_informacion_semanal()

    # Calcular y mostrar el promedio
    promedio = mi_semana.calcular_promedio_semanal()
    print(f"\nEl promedio de la temperatura semanal es: {promedio:.2f}°C")

if __name__ == "__main__":
    main()
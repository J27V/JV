# Programa: Conversión de Dólares a Euros
# Descripción:
# Este programa convierte una cantidad de dinero en dólares a euros usando un tipo de cambio fijo.
# Utiliza diferentes tipos de datos: float, string, boolean.

def convertir_a_euros(cantidad_dolares: float, tasa_cambio: float) -> float:
    """
    Convierte una cantidad de dólares a euros.
    :param cantidad_dolares: Monto en dólares.
    :param tasa_cambio: Valor de 1 dólar en euros.
    :return: Monto equivalente en euros.
    """
    euros = cantidad_dolares * tasa_cambio
    return euros


# Asignar cantidad fija de dólares
dolares = 155.0

# Definir tasa de cambio (ejemplo: 1 dólar = 0.90 euros)
tasa_cambio = 0.90

# Calcular el monto en euros
euros_convertidos = convertir_a_euros(dolares, tasa_cambio)

# Variable booleana: True si la cantidad en euros supera 100
es_monto_grande = euros_convertidos > 100

# Mostrar resultados
print("El equivalente en euros es:", euros_convertidos)
print("¿Es un monto mayor a 100 euros?", es_monto_grande)




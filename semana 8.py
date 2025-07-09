import os
import subprocess


def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n{codigo}")
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None


def ejecutar_codigo(ruta_script):
    try:
        if os.name == 'nt':
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:
            subprocess.Popen(['xterm', '-hold', '-e', f'python3 "{ruta_script}"'])
    except Exception as e:
        print(f"Error al ejecutar el código: {e}")


def mostrar_menu():
    ruta_base = os.path.dirname(os.path.abspath(_file_))

    unidades = {
        '1': 'semana5/tarea.py',
        '2': 'semana6/tarea_s6.py',
        '3': 'semana7/constructores.py',
    }

    while True:
        print("\nMenu Principal - Dashboard")
        for key, path in unidades.items():
            print(f"{key} - {path}")
        print("0 - Salir")

        eleccion_unidad = input("Elige una unidad o '0' para salir: ")
        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, os.path.dirname(unidades[eleccion_unidad])))
        else:
            print("Opción no válida. Intenta nuevamente.")


def mostrar_sub_menu(ruta_unidad):
    try:
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
    except FileNotFoundError:
        print("Ruta de unidad no encontrada.")
        return

    while True:
        print("\nSubmenú - Selecciona una subcarpeta")
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion = input("Elige una opción: ")
        if eleccion == '0':
            break
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(sub_carpetas):
            carpeta_seleccionada = sub_carpetas[int(eleccion) - 1]
            mostrar_scripts(os.path.join(ruta_unidad, carpeta_seleccionada))
        else:
            print("Opción no válida. Intenta nuevamente.")


def mostrar_scripts(ruta_sub_carpeta):
    try:
        scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]
    except FileNotFoundError:
        print("Ruta de carpeta no encontrada.")
        return

    while True:
        print("\nScripts - Selecciona un script para ver y ejecutar")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar al submenú")
        print("9 - Regresar al menú principal")

        eleccion = input("Tu elección: ")
        if eleccion == '0':
            break
        elif eleccion == '9':
            return
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(scripts):
            ruta_script = os.path.join(ruta_sub_carpeta, scripts[int(eleccion) - 1])
            codigo = mostrar_codigo(ruta_script)
            if codigo:
                ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                if ejecutar == '1':
                    ejecutar_codigo(ruta_script)
                elif ejecutar == '0':
                    print("Script no ejecutado.")
                else:
                    print("Opción no válida.")
                input("Presiona Enter para continuar.")
        else:
            print("Opción no válida. Intenta nuevamente.")


if _name_ == "_main_":
    mostrar_menu()
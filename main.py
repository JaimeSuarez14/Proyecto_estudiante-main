import numpy as np 
from clases import Estudiante
from funciones import (
    cargar_estudiantes, guardar_estudiantes,
    buscar_estudiante, eliminar_estudiante, analisis_datos, generar_reporte_pdf
)

def menu():
    print("\033[96m\n--- Sistema de Gestión de Estudiantes ---\033[0m")
    print("\033[92m1. Agregar estudiante\033[0m")
    print("\033[94m2. Buscar estudiante\033[0m")
    print("\033[95m3. Eliminar estudiante\033[0m")
    print("\033[93m4. Análisis de datos\033[0m")
    print("\033[96m6. Generar reporte PDF de un estudiante\033[0m")
    print("\033[91m5. Salir\033[0m")

def main():
    estudiantes = cargar_estudiantes()
    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        # Colores para mensajes y entradas
        rojo = "\033[91m"
        reset = "\033[0m"

        if opcion == "1":
            color = "\033[92m"  
            nombre = input(f"{color}Nombre: {reset}").strip()
            while not any(c.isalpha() for c in nombre):
                print(f"{rojo}Por favor ingresa un texto válido que contenga letras.{reset}")
                nombre = input(f"{color}Nombre: {reset}").strip()

            while True:
                try:
                    edad = int(input(f"{color}Edad: {reset}"))
                    break
                except ValueError:
                    print(f"{rojo}Por favor ingresa un número entero válido.{reset}")

            while True:
                matricula = input(f"{color}Matrícula (U12345678): {reset}").strip()
                if len(matricula) != 9:
                    print(f"{rojo}La matrícula debe tener exactamente 9 caracteres.{reset}")
                    continue
                if buscar_estudiante(estudiantes, matricula):
                    print(f"{rojo}Ya existe un estudiante con esa matrícula.{reset}")
                    continue
                break

            carrera = input(f"{color}Carrera: {reset}").strip()
            while not any(c.isalpha() for c in carrera):
                print(f"{rojo}Por favor ingresa un texto válido que contenga letras.{reset}")
                carrera = input(f"{color}Carrera: {reset}").strip()

            calificaciones = []
            for i in range(3):
                while True:
                    try:
                        cal = float(input(f"{color}Calificación {i+1}: {reset}"))
                        if 0 <= cal <= 20:
                            calificaciones.append(cal)
                            break
                        else:
                            print(f"{rojo}La nota debe estar entre 0 y 20.{reset}")
                    except ValueError:
                        print(f"{rojo}Por favor ingresa un número válido.{reset}")

            while True:
                beca_resp = input(f"{color}¿Tiene beca? (si/no): {reset}").strip().lower()
                if beca_resp in ['si', 'no']:
                    becado = (beca_resp == 'si')
                    break
                print(f"{rojo}Por favor responde solo 'si' o 'no'.{reset}")

            estudiante = Estudiante(nombre, edad, matricula, carrera, calificaciones, becado)
            estudiantes.append(estudiante)
            guardar_estudiantes(estudiantes)
            print(f"{color}Estudiante agregado correctamente.{reset}")

        elif opcion == "2":
            color = "\033[94m"  
            mat = input(f"{color}Matrícula a buscar : {reset}").strip()
            if mat == "":
                if not estudiantes:
                    print(f"{rojo}No hay estudiantes registrados.{reset}")
                else:
                    for e in estudiantes:
                        print(e.mostrar_datos())
            else:
                est = buscar_estudiante(estudiantes, mat)
                if est:
                    print(est.mostrar_datos())
                else:
                    print(f"{rojo}Estudiante no encontrado.{reset}")

        elif opcion == "3":
            color = "\033[95m"  
            mat = input(f"{color}Matrícula a eliminar: {reset}").strip()
            est = buscar_estudiante(estudiantes, mat)
            if est:
                confirm = input(f"{color}¿Seguro que quieres eliminar a {est.nombre}? (si/no): {reset}").strip().lower()
                if confirm == 'si':
                    estudiantes = eliminar_estudiante(estudiantes, mat)
                    guardar_estudiantes(estudiantes)
                    print(f"{color}Estudiante eliminado.{reset}")
                else:
                    print(f"{color}Eliminación cancelada.{reset}")
            else:
                print(f"{rojo}Estudiante no encontrado.{reset}")

        elif opcion == "4":
            color = "\033[93m"  
            print(f"{color}")
            analisis_datos(estudiantes)
            print(reset)

        elif opcion == "6":
            color = "\033[96m"
            mat = input(f"{color}Matrícula del estudiante para el reporte PDF: {reset}").strip()
            est = buscar_estudiante(estudiantes, mat)
            if est:
                generar_reporte_pdf(est)
            else:
                print(f"{rojo}Estudiante no encontrado.{reset}")

        elif opcion == "5":
            print("Saliendo del sistema...")
            break

        else:
            print(f"{rojo}Opción inválida. Intenta de nuevo.{reset}")

if __name__ == "__main__":
    main()

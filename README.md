# Sistema de Gestión de Estudiantes

Este proyecto es una aplicación de consola en Python para gestionar estudiantes, sus calificaciones y realizar análisis de datos básicos. Utiliza archivos CSV para almacenar la información y la biblioteca pandas para el manejo de datos.

## Estructura de Archivos

- `clases.py`
- `estudiantes.csv`
- `funciones.py`
- `main.py`

---

## 1. `clases.py`

Define las clases principales del sistema:

- **Persona**: Clase base con atributos `nombre` y `edad`.
- **Estudiante**: Hereda de `Persona` y añade:
  - `matricula`: Identificador único del estudiante.
  - `calificaciones`: Lista de 3 calificaciones.
  - `promedio()`: Calcula el promedio de las calificaciones usando numpy.
  - `to_dict()`: Devuelve un diccionario con todos los datos del estudiante, útil para guardar y mostrar información.

---

## 2. `estudiantes.csv`

Archivo donde se almacena la información de los estudiantes en formato de tabla.  
**Columnas:**
- `Nombre`: Nombre del estudiante.
- `Edad`: Edad del estudiante.
- `Matrícula`: Identificador único.
- `Cal1`, `Cal2`, `Cal3`: Calificaciones del estudiante.
- `Promedio`: Promedio de las tres calificaciones.

**Ejemplo de contenido:**
```
Nombre,Edad,Matrícula,Cal1,Cal2,Cal3,Promedio
Juan Pérez,20,2023001,85.0,90.0,88.0,87.66666666666667
María García,19,2023002,92.0,88.0,95.0,91.66666666666667
...
```

---

## 3. `funciones.py`

Contiene funciones auxiliares para manipular la información de los estudiantes:

- **cargar_estudiantes()**:  
  Lee el archivo CSV y crea una lista de objetos `Estudiante`. Si el archivo está vacío, retorna una lista vacía.

- **guardar_estudiantes(estudiantes)**:  
  Guarda la lista de estudiantes en el archivo CSV, convirtiendo cada objeto a diccionario.

- **mostrar_estudiantes(estudiantes)**:  
  Imprime en pantalla la información de todos los estudiantes.

- **buscar_estudiante(estudiantes, matricula)**:  
  Busca y retorna un estudiante por su matrícula.

- **eliminar_estudiante(estudiantes, matricula)**:  
  Elimina un estudiante de la lista según su matrícula.

- **analisis_datos(estudiantes)**:  
  Muestra una tabla con todos los estudiantes y realiza análisis como:
  - Edad promedio.
  - Promedio general de notas.
  - Nombre del estudiante con mayor promedio.

---

## 4. `main.py`

Archivo principal que ejecuta el programa y muestra un menú interactivo:

- **menu()**:  
  Muestra las opciones disponibles al usuario.

- **main()**:  
  - Carga los estudiantes desde el archivo CSV.
  - Muestra el menú y espera la selección del usuario.
  - Permite:
    1. Agregar un nuevo estudiante (pide datos por consola y guarda en el CSV).
    2. Mostrar todos los estudiantes.
    3. Buscar un estudiante por matrícula.
    4. Eliminar un estudiante por matrícula.
    5. Realizar análisis de datos.
    6. Salir del sistema.

- El programa se ejecuta en bucle hasta que el usuario elige salir.

---

## Requisitos

- Python 3.x
- pandas
- numpy

Instala las dependencias con:
```bash
pip install pandas numpy
```

---

## Uso

Ejecuta el programa principal:
```bash
python main.py
```

Sigue las instrucciones del menú para gestionar los estudiantes. 
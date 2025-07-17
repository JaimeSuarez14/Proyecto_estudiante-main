import numpy as np
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
class Estudiante(Persona):
    def __init__(self, nombre, edad, matricula, carrera, calificaciones, becado=False):
        super().__init__(nombre, edad)
        self.matricula = matricula
        self.carrera = carrera
        self.calificaciones = calificaciones  # Lista [c1, c2, c3]
        self.becado = becado  # Nuevo atributo
    def promedio(self):
        return np.mean(self.calificaciones)
    def es_aprobado(self):
        return self.promedio() >= 13
    def mostrar_datos(self):
        beca_str = "Sí" if self.becado else "No"
        return (f"Nombre: {self.nombre}, Edad: {self.edad}, Matrícula: {self.matricula}, "
                f"Carrera: {self.carrera}, Notas: {self.calificaciones}, "
                f"Promedio: {self.promedio():.2f}, Becado: {beca_str}, "
                f"Aprobado: {'Sí' if self.es_aprobado() else 'No'}")
    def to_dict(self):
        return {
            'Nombre': self.nombre,
            'Edad': self.edad,
            'Matrícula': self.matricula,
            'Carrera': self.carrera,
            'Cal1': self.calificaciones[0],
            'Cal2': self.calificaciones[1],
            'Cal3': self.calificaciones[2],
            'Promedio': self.promedio(),
            'Becado': 'Sí' if self.becado else 'No',
            'Aprobado': 'Sí' if self.es_aprobado() else 'No'
        }
class Becado(Estudiante):
    def __init__(self, nombre, edad, matricula, carrera, calificaciones):
        super().__init__(nombre, edad, matricula, carrera, calificaciones, becado=True)
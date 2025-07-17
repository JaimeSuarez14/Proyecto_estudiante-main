import tkinter as tk
from tkinter import simpledialog, messagebox
from funciones import (
    cargar_estudiantes,
    guardar_estudiantes,
    buscar_estudiante,
    eliminar_estudiante,
    analisis_datos
)
from clases import Estudiante  
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Estudiantes")
        self.estudiantes = cargar_estudiantes()
        tk.Button(root, text="Agregar estudiante", command=self.agregar_estudiante).pack(fill='x')
        tk.Button(root, text="Mostrar estudiantes", command=self.mostrar_estudiantes).pack(fill='x')
        tk.Button(root, text="Buscar estudiante", command=self.buscar_estudiante).pack(fill='x')
        tk.Button(root, text="Eliminar estudiante", command=self.eliminar_estudiante).pack(fill='x')
        tk.Button(root, text="Análisis de datos", command=self.analisis_datos).pack(fill='x')
        tk.Button(root, text="Salir", command=root.quit).pack(fill='x')
    def agregar_estudiante(self):
        nombre = simpledialog.askstring("Nombre", "Nombre del estudiante:")
        if not nombre:
            return
        edad = simpledialog.askinteger("Edad", "Edad del estudiante:")
        if edad is None:
            return
        matricula = simpledialog.askstring("Matrícula", "Matrícula del estudiante:")
        if not matricula:
            return
        carrera = simpledialog.askstring("Carrera", "Carrera del estudiante:")
        if not carrera:
            return
        calificaciones = []
        for i in range(3):
            cal = simpledialog.askfloat("Calificación", f"Calificación {i+1}:")
            if cal is None:
                return
            calificaciones.append(cal)
        beca_resp = simpledialog.askstring("Beca", "¿Tiene beca? (sí/no):")
        becado = beca_resp and beca_resp.strip().lower() == 'sí'

        estudiante = Estudiante(nombre, edad, matricula, carrera, calificaciones, becado)
        self.estudiantes.append(estudiante)
        guardar_estudiantes(self.estudiantes)
        messagebox.showinfo("Éxito", "Estudiante agregado correctamente.")
    def mostrar_estudiantes(self):
        if not self.estudiantes:
            messagebox.showinfo("Estudiantes", "No hay estudiantes registrados.")
            return
        texto = ""
        for e in self.estudiantes:
            texto += str(e.to_dict()) + "\n"
        messagebox.showinfo("Estudiantes", texto)
    def buscar_estudiante(self):
        matricula = simpledialog.askstring("Buscar", "Matrícula a buscar:")
        if not matricula:
            return
        est = buscar_estudiante(self.estudiantes, matricula)
        if est:
            messagebox.showinfo("Encontrado", str(est.to_dict()))
        else:
            messagebox.showwarning("No encontrado", "Estudiante no encontrado.")
    def eliminar_estudiante(self):
        matricula = simpledialog.askstring("Eliminar", "Matrícula a eliminar:")
        if not matricula:
            return
        self.estudiantes = eliminar_estudiante(self.estudiantes, matricula)
        guardar_estudiantes(self.estudiantes)
        messagebox.showinfo("Eliminado", "Estudiante eliminado.")
    def analisis_datos(self):
        analisis_datos(self.estudiantes)
        messagebox.showinfo("Análisis", "Consulta la consola para ver el análisis de datos.")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()
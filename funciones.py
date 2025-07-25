import numpy as np
import pandas as pd
import os
from clases import Estudiante
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

ARCHIVO_CSV = "estudiantes.csv"

def cargar_estudiantes():
    estudiantes = []
    if os.path.exists(ARCHIVO_CSV):
        df = pd.read_csv(ARCHIVO_CSV)
        for _, row in df.iterrows():
            try:
                nombre = row['Nombre']
                edad = int(row['Edad'])
                matricula = str(row['Matrícula'])
                carrera = row['Carrera'] if 'Carrera' in row else "Sin especificar"
                cal1 = float(row['Cal1'])
                cal2 = float(row['Cal2'])
                cal3 = float(row['Cal3'])
                calificaciones = [cal1, cal2, cal3]
                becado = str(row.get('Becado', 'No')).strip().lower() == 'sí'

                estudiante = Estudiante(nombre, edad, matricula, carrera, calificaciones, becado)
                estudiantes.append(estudiante)
            except Exception as e:
                print(f"[Error al cargar estudiante] {e}")
    return estudiantes

def guardar_estudiantes(estudiantes):
    data = [e.to_dict() for e in estudiantes]
    df = pd.DataFrame(data)
    df.to_csv(ARCHIVO_CSV, index=False)

def mostrar_estudiantes(estudiantes):
    for e in estudiantes:
        print(e.to_dict())

def buscar_estudiante(estudiantes, matricula):
    return next((e for e in estudiantes if e.matricula == matricula), None)

def buscar_estudiantes_por_carrera(estudiantes, carrera_buscar):
    carrera_buscar = carrera_buscar.lower()
    return [e for e in estudiantes if carrera_buscar in e.carrera.lower()]

def eliminar_estudiante(estudiantes, matricula):
    return [e for e in estudiantes if e.matricula != matricula]

def generar_reporte_analisis_pdf(estudiantes):
    if not estudiantes:
        print("No hay estudiantes para generar el reporte.")
        return None

    pdf_filename = "reporte_analisis_general.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    styles.add(ParagraphStyle(name='SectionHeading',
                              parent=styles['h2'],
                              fontSize=14,
                              leading=18,
                              spaceAfter=6,
                              textColor=colors.darkblue))

    title_style = styles['Title']
    title_style.alignment = 1  
    story.append(Paragraph("Reporte de Análisis General de Estudiantes", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 0.3 * inch))

    df = pd.DataFrame([e.to_dict() for e in estudiantes])

    df.insert(0, 'N°', range(1, len(df) + 1))

    columnas = list(df.columns)
    datos_tabla = [columnas] + df.round(2).astype(str).values.tolist()

    tabla_estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E8B57')),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5DC')),  
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    tabla = Table(datos_tabla, hAlign='CENTER')
    tabla.setStyle(tabla_estilo)
    story.append(Paragraph("Tabla de Estudiantes", styles['SectionHeading']))
    story.append(tabla)
    story.append(Spacer(1, 0.4 * inch))

    
    story.append(Paragraph("Estadísticas Generales", styles['SectionHeading']))

    promedio_general = df['Promedio'].mean()
    desviacion_std = df['Promedio'].std()
    nota_maxima = df[['Cal1', 'Cal2', 'Cal3']].max().max()
    nota_minima = df[['Cal1', 'Cal2', 'Cal3']].min().min()
    nombre_mejor = df.loc[df['Promedio'].idxmax()]['Nombre']
    aprobados = sum(1 for e in estudiantes if e.es_aprobado())
    desaprobados = len(estudiantes) - aprobados

    texto_estadisticas = (
        f"<b>Promedio general de notas:</b> {promedio_general:.2f}<br/>"
        f"<b>Desviación estándar del promedio:</b> {desviacion_std:.2f}<br/>"
        f"<b>Nota máxima del grupo:</b> {nota_maxima:.2f}<br/>"
        f"<b>Nota mínima del grupo:</b> {nota_minima:.2f}<br/>"
        f"<b>Estudiante con mayor promedio:</b> {nombre_mejor}<br/>"
        f"<b>Cantidad de estudiantes aprobados:</b> {aprobados}<br/>"
        f"<b>Cantidad de estudiantes desaprobados:</b> {desaprobados}<br/>"
    )
    story.append(Paragraph(texto_estadisticas, styles['Normal']))

    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Reporte generado por el Sistema de Gestión de Estudiantes de Data Max.", styles['Italic']))
    story.append(Paragraph(f"Fecha de generación: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))

    try:
        doc.build(story)
        print(f"Reporte PDF generado exitosamente: {pdf_filename}")
        return pdf_filename
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        return None

def analisis_datos(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    generar_reporte_analisis_pdf(estudiantes)


def generar_reporte_pdf(estudiante):
    if not estudiante:
        print("No se puede generar reporte: Estudiante no proporcionado.")
        return None

    pdf_filename = f"reporte_estudiante_{estudiante.matricula}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Estilos personalizados ---
    # Estilo para subtítulos/encabezados de sección
    styles.add(ParagraphStyle(name='SectionHeading',
                              parent=styles['h2'],
                              fontSize=14,
                              leading=18,
                              spaceAfter=6,
                              textColor=colors.darkblue))
    
    # Estilo para el estado de aprobación
    styles.add(ParagraphStyle(name='StatusApproved',
                              parent=styles['Normal'],
                              textColor=colors.HexColor('#006400'), # Verde oscuro
                              fontName='Helvetica-Bold',
                              fontSize=11))
    styles.add(ParagraphStyle(name='StatusFailed',
                              parent=styles['Normal'],
                              textColor=colors.HexColor('#8B0000'), # Rojo oscuro
                              fontName='Helvetica-Bold',
                              fontSize=11))

    # --- Cabecera del Reporte ---
    # Título principal del documento
    title_style = styles['Title']
    title_style.alignment = 1 # Center
    story.append(Paragraph("Reporte Académico Individual", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceBefore=0, spaceAfter=0, hAlign='CENTER', vAlign='BOTTOM'))
    story.append(Spacer(1, 0.2 * inch))

    # --- Información General del Estudiante ---
    story.append(Paragraph("Información General del Estudiante", styles['SectionHeading']))
    story.append(Paragraph(f"<b>Nombre:</b> {estudiante.nombre}", styles['Normal']))
    story.append(Paragraph(f"<b>Edad:</b> {estudiante.edad}", styles['Normal']))
    story.append(Paragraph(f"<b>Matrícula:</b> {estudiante.matricula}", styles['Normal']))
    story.append(Paragraph(f"<b>Carrera:</b> {estudiante.carrera}", styles['Normal']))
    story.append(Paragraph(f"<b>Becado:</b> {'Sí' if estudiante.becado else 'No'}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # --- Detalle de Calificaciones ---
    story.append(Paragraph("Detalle de Calificaciones", styles['SectionHeading']))
    data_calificaciones = [['Materia/Evaluación', 'Nota']]
    for i, cal in enumerate(estudiante.calificaciones):
        data_calificaciones.append([f'Calificación {i+1}', f'{cal:.2f}'])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E8B57')), # Verde mar oscuro
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5DC')), # Beige claro
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])

    table_calificaciones = Table(data_calificaciones)
    table_calificaciones.setStyle(table_style)
    story.append(table_calificaciones)
    story.append(Spacer(1, 0.5 * inch))

    # --- Resumen de Rendimiento ---
    story.append(Paragraph("Resumen de Rendimiento Académico", styles['SectionHeading']))
    story.append(Paragraph(f"El promedio general del estudiante es: <b>{estudiante.promedio():.2f}</b>.", styles['Normal']))
    
    if estudiante.es_aprobado():
        story.append(Paragraph(f"Con un promedio de {estudiante.promedio():.2f} (nota mínima aprobatoria: 13), el estudiante ha obtenido el estado de: <font color='green'><b>APROBADO</b></font>.", styles['StatusApproved']))
    else:
        story.append(Paragraph(f"Con un promedio de {estudiante.promedio():.2f} (nota mínima aprobatoria: 13), el estudiante ha obtenido el estado de: <font color='red'><b>DESAPROBADO</b></font>.", styles['StatusFailed']))
    
    story.append(Spacer(1, 0.5 * inch))

    # --- Pie de página ---
    story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceBefore=0, spaceAfter=0, hAlign='CENTER', vAlign='BOTTOM'))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"Reporte generado por el Sistema de Gestión de Estudiantes de Data Max.", styles['Italic']))
    story.append(Paragraph(f"Fecha de generación: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))

    try:
        doc.build(story)
        print(f"Reporte PDF generado exitosamente: {pdf_filename}")
        return pdf_filename
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        return None

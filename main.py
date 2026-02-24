from fastapi import FastAPI
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

app = FastAPI()

SHEET_ID = "1MJ-zBEaLm-TbRjZlKw_8MdfhWGshfQ4gfxIke6Wbw88"

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# 🔐 Cargar credenciales desde variable de entorno (Render)
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)

client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID)

@app.post("/guardar-reporte")
def guardar_reporte(data: dict):

    fecha = datetime.now().strftime("%d/%m/%Y")

    # -------- HOJA 1: REPORTE INDIVIDUAL --------
    hoja1 = sheet.worksheet("REPORTE INDIVIDUAL")
    hoja1.append_row([
        fecha,
        data.get("estudiante"),
        data.get("curso"),
        data.get("tipo_documento"),
        data.get("cumple_estructura"),
        data.get("observaciones")
    ])

    # -------- HOJA 2: DETALLE ESTRUCTURA --------
    hoja2 = sheet.worksheet("DETALLE ESTRUCTURA")
    hoja2.append_row([
        data.get("estudiante"),
        data.get("introduccion_ok"),
        data.get("antecedentes_ok"),
        data.get("problema_ok"),
        data.get("justificacion_ok"),
        data.get("objetivos_ok"),
        data.get("marco_conceptual_ok"),
        data.get("marco_metodologico_ok"),
        data.get("resultados_ok"),
        data.get("analisis_ok"),
        data.get("conclusiones_ok"),
        data.get("recomendaciones_ok"),
        data.get("referencias_ok"),
        data.get("anexos_ok")
    ])

    # -------- HOJA 3: CONTROL PALABRAS --------
    hoja3 = sheet.worksheet("CONTROL PALABRAS")
    hoja3.append_row([
        data.get("estudiante"),
        data.get("palabras_intro"),
        data.get("palabras_anteced"),
        data.get("palabras_problema"),
        data.get("palabras_justif"),
        data.get("palabras_obj"),
        data.get("palabras_marco_c"),
        data.get("palabras_marco_m"),
        data.get("palabras_result"),
        data.get("palabras_analisis"),
        data.get("palabras_concl"),
        data.get("palabras_recom")
    ])

    return {"status": "Reporte completo guardado correctamente"}

from fastapi.responses import JSONResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import base64

@app.post("/generar-pdf")
def generar_pdf(data: dict):

    estudiante = str(data.get("estudiante", "No especificado"))
    curso = str(data.get("curso", "No especificado"))
    observaciones = str(data.get("observaciones", ""))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("ANÁLISIS DE PROYECTO DOCUMENTO DE GRADO", styles["Heading1"]))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"Estudiante: {estudiante}", styles["Normal"]))
    elements.append(Paragraph(f"Curso: {curso}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Observaciones:", styles["Heading2"]))
    elements.append(Paragraph(observaciones, styles["Normal"]))

    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    return JSONResponse({
        "file_name": "analisis.pdf",
        "file_base64": pdf_base64
    })

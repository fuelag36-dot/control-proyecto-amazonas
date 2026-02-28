from fastapi import FastAPI
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

app = FastAPI()
@app.get("/")
def home():
    return {"status": "API control-proyecto-amazonas activa"}
@app.get("/health")
def health():
    return {"ok": True}
    
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

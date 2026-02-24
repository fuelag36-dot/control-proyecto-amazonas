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

    hoja1 = sheet.worksheet("REPORTE INDIVIDUAL")
    hoja1.append_row([
        fecha,
        data["estudiante"],
        data["curso"],
        data["tipo_documento"],
        data["cumple_estructura"],
        data["observaciones"]
    ])

    return {"status": "Reporte guardado correctamente"}

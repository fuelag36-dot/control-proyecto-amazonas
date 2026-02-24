from fastapi import FastAPI
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = FastAPI()

SHEET_ID = "1MJ-zBEaLm-TbRjZlKw_8MdfhWGshfQ4gfxIke6Wbw88"
CREDS_FILE = "proyecto-control-bgu-amazonas-2fa210665b3d.json"

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file(CREDS_FILE, scopes=scopes)
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
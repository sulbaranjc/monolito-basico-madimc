from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from datetime import datetime, date
from typing import Dict, Any, Optional

app = FastAPI(title="MEDIMIC Monolith (MVP)", version="0.1.0")
templates = Jinja2Templates(directory="app/templates")

# ============================
# 📦 "Base de datos" en memoria
# ============================
PATIENTS: Dict[str, Dict[str, Any]] = {}


# ============================
# 🔧 Helpers (lógica de dominio)
# ============================

def normalize_name(value: str) -> str:
    # Normaliza el nombre: quita espacios extra y aplica Capitalización Tipo Título
    value = " ".join(value.strip().split())
    return value.title()

def calculate_age_years(dob: date) -> int:
    # Calcula edad en años truncados respecto a la fecha actual
    today = date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return max(0, years)

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    # Calcula el IMC = peso(kg) / (altura(m)^2) y redondea a 2 decimales
    h_m = height_cm / 100.0
    return round(weight_kg / (h_m ** 2), 2)

def bmi_category(bmi: float) -> str:
    # Determina la categoría OMS del IMC
    if bmi < 18.5:
        return "bajo peso"
    if bmi < 25.0:
        return "normal"
    if bmi < 30.0:
        return "sobrepeso"
    return "obesidad"


# ============================
# 🌡 Healthcheck sencillo
# ============================
@app.get("/health", response_class=HTMLResponse)
def health(_: Request):
    # Respuesta mínima para verificar que el servicio está arriba
    return "<pre>{\"status\":\"ok\"}</pre>"


# ============================
# 👤 Vistas de Paciente (crear)
# ============================

# GET: muestra formulario de creación
@app.get("/patients/create", response_class=HTMLResponse)
def get_create_patient(request: Request):
    # Renderiza el formulario vacío
    return templates.TemplateResponse(
        "create_patient.html",
        {
            "request": request,
            "form_data": {},
            "errors": [],
            "result": None,
        },
    )

# POST: procesa formulario, valida, calcula IMC y muestra resultado
@app.post("/patients/create", response_class=HTMLResponse)
async def post_create_patient(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: str = Form(...),  # ISO (yyyy-mm-dd) desde <input type="date">
    sex_at_birth: str = Form(...),   # 'male' | 'female' | 'other'
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    height_cm: Optional[str] = Form(None),
    weight_kg: Optional[str] = Form(None),
    consent_data_processing: Optional[str] = Form(None),  # "on" si está marcado
):
    # --- Validaciones básicas de formulario ---
    errors = []

    # Normalizamos nombres para consistencia visual
    first_name_norm = normalize_name(first_name)
    last_name_norm = normalize_name(last_name)

    # Consentimiento obligatorio (GDPR-friendly)
    if consent_data_processing != "on":
        errors.append("Debes aceptar el consentimiento de procesamiento de datos.")

    # Validación de fecha de nacimiento (formato y que sea pasada)
    dob_obj: Optional[date] = None
    try:
        dob_obj = date.fromisoformat(date_of_birth)
        if dob_obj > date.today():
            errors.append("La fecha de nacimiento debe estar en el pasado.")
    except Exception:
        errors.append("Formato de fecha inválido. Usa AAAA-MM-DD.")

    # Validación de sexo al nacer (controlado por select)
    if sex_at_birth not in {"male", "female", "other"}:
        errors.append("El campo 'Sexo al nacer' es inválido.")

    # Email/teléfono son opcionales; chequeos mínimos didácticos
    if email and "@" not in email:
        errors.append("El correo electrónico no es válido.")
    if phone and len(phone) < 7:
        errors.append("El número de teléfono parece demasiado corto.")

    # Parseo de altura/peso (opcionales); si ambos están, luego calculamos IMC
    height_val: Optional[float] = None
    weight_val: Optional[float] = None

    def parse_float_or_none(v: Optional[str]) -> Optional[float]:
        # Convierte string a float o None si viene vacío
        if v is None or v.strip() == "":
            return None
        return float(v)

    try:
        height_val = parse_float_or_none(height_cm)
        weight_val = parse_float_or_none(weight_kg)
    except ValueError:
        errors.append("La altura y el peso deben ser valores numéricos.")

    # Rango razonable para evitar datos basura
    if height_val is not None and not (100.0 <= height_val <= 250.0):
        errors.append("La altura (cm) debe estar entre 100 y 250.")
    if weight_val is not None and not (20.0 <= weight_val <= 300.0):
        errors.append("El peso (kg) debe estar entre 20 y 300.")

    # Si hay errores, re-renderizamos el formulario con mensajes y valores previos
    if errors:
        return templates.TemplateResponse(
            "create_patient.html",
            {
                "request": request,
                "form_data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": date_of_birth,
                    "sex_at_birth": sex_at_birth,
                    "email": email,
                    "phone": phone,
                    "height_cm": height_cm,
                    "weight_kg": weight_kg,
                    "consent_data_processing": consent_data_processing == "on",
                },
                "errors": errors,
                "result": None,
            },
            status_code=400,
        )

    # --- Construimos el registro del paciente (persistencia en memoria) ---
    patient_id = str(uuid4())
    now = datetime.utcnow().isoformat() + "Z"

    patient_record: Dict[str, Any] = {
        # Identidad y metadatos
        "patient_id": patient_id,
        "first_name": first_name_norm,
        "last_name": last_name_norm,
        "date_of_birth": dob_obj.isoformat() if dob_obj else None,
        "sex_at_birth": sex_at_birth,
        "email": email or None,
        "phone": phone or None,
        "consent_data_processing": True,
        "created_at": now,
        "updated_at": now,
        # Entradas y salidas de IMC (última lectura)
        "height_cm": height_val,
        "weight_kg": weight_val,
        "bmi_inputs_updated_at": None,
        "bmi_last": None,
        "bmi_category_last": None,
        "bmi_last_measured_at": None,
        # Conveniencias calculadas para UI
        "computed": {
            "display_name": f"{last_name_norm}, {first_name_norm}",
            "age_years": calculate_age_years(dob_obj) if dob_obj else None,
            "is_adult": (calculate_age_years(dob_obj) >= 18) if dob_obj else None,
            "contactable": bool((email and email.strip()) or (phone and phone.strip())),
        },
    }

    # Si tenemos altura y peso, calculamos IMC y su categoría
    if (height_val is not None) and (weight_val is not None):
        bmi_val = calculate_bmi(weight_val, height_val)
        patient_record["bmi_last"] = bmi_val
        patient_record["bmi_category_last"] = bmi_category(bmi_val)
        patient_record["bmi_last_measured_at"] = now
        patient_record["bmi_inputs_updated_at"] = now

    # Guardamos en la "BD" en memoria
    PATIENTS[patient_id] = patient_record

    # Renderizamos la misma vista con el resultado
    return templates.TemplateResponse(
        "create_patient.html",
        {
            "request": request,
            "form_data": {
                "first_name": first_name_norm,
                "last_name": last_name_norm,
                "date_of_birth": patient_record["date_of_birth"],
                "sex_at_birth": sex_at_birth,
                "email": email,
                "phone": phone,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "consent_data_processing": True,
            },
            "errors": [],
            "result": {
                "patient_id": patient_id,
                "display_name": patient_record["computed"]["display_name"],
                "age_years": patient_record["computed"]["age_years"],
                "sex_at_birth": sex_at_birth,
                "bmi_last": patient_record["bmi_last"],
                "bmi_category_last": patient_record["bmi_category_last"],
            },
        },
    )

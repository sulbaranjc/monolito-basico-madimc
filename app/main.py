# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from datetime import datetime, date
from typing import Dict, Any, Optional
from pathlib import Path

from app.data.patients_seed import SEEDED_PATIENTS

# ============================
# 🚀 App base
# ============================
app = FastAPI(title="MEDIMIC Monolith (MVP)", version="0.1.3")

# ============================
# 🗂️ Rutas absolutas (templates / static)
# ============================
BASE_DIR = Path(__file__).resolve().parent            # .../app
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ============================
# 📦 "Base de datos" en memoria
# ============================
PATIENTS: Dict[str, Dict[str, Any]] = dict(SEEDED_PATIENTS)

# 🔁 Migración en caliente del seed (si vino en inglés -> español)
_SEX_EN_TO_ES = {"male": "Masculino", "female": "Femenino", "other": "Otro"}
for _p in PATIENTS.values():
    v = (_p.get("sex_at_birth") or "").strip().lower()
    if v in _SEX_EN_TO_ES:
        _p["sex_at_birth"] = _SEX_EN_TO_ES[v]

# ============================
# 🔧 Helpers de dominio (comentarios en español, código en inglés)
# ============================
def normalize_name(value: str) -> str:
    # Normaliza el nombre: quita espacios extra y aplica Capitalización Tipo Título
    value = " ".join(value.strip().split())
    return value.title()

def calculate_age_years(dob: date) -> int:
    today = date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return max(0, years)

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100.0
    return round(weight_kg / (h_m ** 2), 2)

def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "bajo peso"
    if bmi < 25.0:
        return "normal"
    if bmi < 30.0:
        return "sobrepeso"
    return "obesidad"

# ============================
# 🌡 Healthcheck
# ============================
@app.get("/health", response_class=HTMLResponse)
def health(_: Request):
    return "<pre>{\"status\":\"ok\"}</pre>"

# ============================
# 👤 Vistas de Paciente (crear)
# ============================
@app.get("/patients/create", response_class=HTMLResponse)
def get_create_patient(request: Request):
    return templates.TemplateResponse(
        "patients_create.html",
        {"request": request, "form_data": {}, "errors": []},
    )

# ============================
# 📨 Vistas de Paciente (crear) - Procesar formulario
# ============================
@app.post("/patients/create", response_class=HTMLResponse)
async def post_create_patient(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: str = Form(...),  # AAAA-MM-DD
    sex_at_birth: str = Form(...),   # 'Masculino' | 'Femenino' | 'Otro'
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    height_cm: Optional[str] = Form(None),
    weight_kg: Optional[str] = Form(None),
    consent_data_processing: Optional[str] = Form(None),  # "on" si marcado
):
    errors = []

    # Normalización de nombres
    first_name_norm = normalize_name(first_name)
    last_name_norm = normalize_name(last_name)

    # Consentimiento obligatorio
    if consent_data_processing != "on":
        errors.append("Debes aceptar el consentimiento para el tratamiento de datos.")

    # Fecha de nacimiento
    dob_obj: Optional[date] = None
    try:
        dob_obj = date.fromisoformat(date_of_birth)
        if dob_obj > date.today():
            errors.append("La fecha de nacimiento debe estar en el pasado.")
    except Exception:
        errors.append("Formato de fecha inválido. Usa AAAA-MM-DD.")

    # --- Sexo al nacer: validar (es) y normalizar a Mayúscula inicial ---
    raw_sex = (sex_at_birth or "").strip()
    sex_lc = raw_sex.lower()
    allowed_sex_es = {"masculino", "femenino", "otro"}
    if sex_lc not in allowed_sex_es:
        errors.append("El campo 'Sexo al nacer' es inválido.")
    # Valor final a persistir (con mayúscula inicial)
    sex_value = {"masculino": "Masculino", "femenino": "Femenino", "otro": "Otro"}.get(sex_lc, raw_sex)

    # Email / teléfono
    if email and "@" not in email:
        errors.append("El correo electrónico no es válido.")
    if phone and len(phone) < 7:
        errors.append("El número de teléfono parece demasiado corto.")

    # Conversión numérica segura
    def parse_float_or_none(v: Optional[str]) -> Optional[float]:
        if v is None or v.strip() == "":
            return None
        return float(v)

    height_val: Optional[float] = None
    weight_val: Optional[float] = None
    try:
        height_val = parse_float_or_none(height_cm)
        weight_val = parse_float_or_none(weight_kg)
    except ValueError:
        errors.append("La altura y el peso deben ser valores numéricos.")

    # Rangos razonables
    if height_val is not None and not (100.0 <= height_val <= 250.0):
        errors.append("La altura (cm) debe estar entre 100 y 250.")
    if weight_val is not None and not (20.0 <= weight_val <= 300.0):
        errors.append("El peso (kg) debe estar entre 20 y 300.")

    # Si hay errores
    if errors:
        return templates.TemplateResponse(
            "patients_create.html",
            {
                "request": request,
                "form_data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": date_of_birth,
                    "sex_at_birth": sex_value,
                    "email": email,
                    "phone": phone,
                    "height_cm": height_cm,
                    "weight_kg": weight_kg,
                    "consent_data_processing": consent_data_processing == "on",
                },
                "errors": errors,
            },
            status_code=400,
        )

    # --- Registro del paciente ---
    patient_id = str(uuid4())
    now = datetime.utcnow().isoformat() + "Z"

    record: Dict[str, Any] = {
        "patient_id": patient_id,
        "first_name": first_name_norm,
        "last_name": last_name_norm,
        "date_of_birth": dob_obj.isoformat() if dob_obj else None,
        "sex_at_birth": sex_value,  # 💾 Se guarda con mayúscula inicial
        "email": email or None,
        "phone": phone or None,
        "consent_data_processing": True,
        "created_at": now,
        "updated_at": now,
        "height_cm": height_val,
        "weight_kg": weight_val,
        "bmi_inputs_updated_at": None,
        "bmi_last": None,
        "bmi_category_last": None,
        "bmi_last_measured_at": None,
        "computed": {
            "display_name": f"{last_name_norm}, {first_name_norm}",
            "age_years": calculate_age_years(dob_obj) if dob_obj else None,
            "is_adult": (calculate_age_years(dob_obj) >= 18) if dob_obj else None,
            "contactable": bool((email and email.strip()) or (phone and phone.strip())),
        },
    }

    # Calcular IMC si aplica
    if (height_val is not None) and (weight_val is not None):
        bmi_val = calculate_bmi(weight_val, height_val)
        record["bmi_last"] = bmi_val
        record["bmi_category_last"] = bmi_category(bmi_val)
        record["bmi_last_measured_at"] = now
        record["bmi_inputs_updated_at"] = now

    # Guardar en memoria
    PATIENTS[patient_id] = record

    # PRG redirect
    return RedirectResponse(url="/patients", status_code=303)

# ============================
# 👥 Vistas de Pacientes (listado)
# ============================
@app.get("/patients", response_class=HTMLResponse)
def list_patients(request: Request):
    patients_sorted = sorted(
        PATIENTS.values(), key=lambda p: (p["last_name"], p["first_name"])
    )
    return templates.TemplateResponse(
        "patients_list.html",
        {"request": request, "patients": patients_sorted},
    )
# ============================
# 🗑️ Eliminar paciente (in-memory)
# ============================
@app.post("/patients/{patient_id}/delete")
def delete_patient(request: Request, patient_id: str):
    # Eliminación segura en memoria; si no existe, no rompe
    PATIENTS.pop(patient_id, None)
    # PRG: tras eliminar, volvemos al listado
    return RedirectResponse(url="/patients", status_code=303)

# ============================
# ✏️ Editar paciente (GET formulario)
# ============================
@app.get("/patients/{patient_id}/edit", response_class=HTMLResponse)
def get_edit_patient(request: Request, patient_id: str):
    # Buscar paciente; si no existe, 404 simple (mensaje didáctico)
    patient = PATIENTS.get(patient_id)
    if not patient:
        return HTMLResponse(
            content=f"<h3>Paciente no encontrado</h3><p>ID: {patient_id}</p>",
            status_code=404,
        )

    # Preparamos form_data con los datos existentes
    form_data = {
        "first_name": patient.get("first_name") or "",
        "last_name": patient.get("last_name") or "",
        "date_of_birth": patient.get("date_of_birth") or "",
        "sex_at_birth": patient.get("sex_at_birth") or "",  # 'Masculino' | 'Femenino' | 'Otro'
        "email": patient.get("email") or "",
        "phone": patient.get("phone") or "",
        "height_cm": "" if patient.get("height_cm") is None else str(patient.get("height_cm")),
        "weight_kg": "" if patient.get("weight_kg") is None else str(patient.get("weight_kg")),
        "consent_data_processing": bool(patient.get("consent_data_processing")),
    }

    return templates.TemplateResponse(
        "patients_edit.html",
        {
            "request": request,
            "patient_id": patient_id,
            "form_data": form_data,
            "errors": [],
        },
    )


# ============================
# 💾 Editar paciente (POST procesar)
# ============================
@app.post("/patients/{patient_id}/edit", response_class=HTMLResponse)
async def post_edit_patient(
    request: Request,
    patient_id: str,
    first_name: str = Form(...),
    last_name: str = Form(...),
    date_of_birth: str = Form(...),  # AAAA-MM-DD
    sex_at_birth: str = Form(...),   # 'Masculino' | 'Femenino' | 'Otro'
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    height_cm: Optional[str] = Form(None),
    weight_kg: Optional[str] = Form(None),
    consent_data_processing: Optional[str] = Form(None),  # "on" si marcado
):
    # Verificamos existencia
    patient = PATIENTS.get(patient_id)
    if not patient:
        return HTMLResponse(
            content=f"<h3>Paciente no encontrado</h3><p>ID: {patient_id}</p>",
            status_code=404,
        )

    # --- Validaciones (idénticas a crear) ---
    errors = []

    first_name_norm = normalize_name(first_name)
    last_name_norm  = normalize_name(last_name)

    if consent_data_processing != "on":
        errors.append("Debes aceptar el consentimiento para el tratamiento de datos.")

    dob_obj: Optional[date] = None
    try:
        dob_obj = date.fromisoformat(date_of_birth)
        if dob_obj > date.today():
            errors.append("La fecha de nacimiento debe estar en el pasado.")
    except Exception:
        errors.append("Formato de fecha inválido. Usa AAAA-MM-DD.")

    # Sexo al nacer: validar y normalizar a Mayúscula inicial
    raw_sex = (sex_at_birth or "").strip()
    sex_lc = raw_sex.lower()
    allowed_sex_es = {"masculino", "femenino", "otro"}
    if sex_lc not in allowed_sex_es:
        errors.append("El campo 'Sexo al nacer' es inválido.")
    sex_value = {"masculino": "Masculino", "femenino": "Femenino", "otro": "Otro"}[sex_lc]

    if email and "@" not in email:
        errors.append("El correo electrónico no es válido.")
    if phone and len(phone) < 7:
        errors.append("El número de teléfono parece demasiado corto.")

    def parse_float_or_none(v: Optional[str]) -> Optional[float]:
        if v is None or v.strip() == "":
            return None
        return float(v)

    height_val: Optional[float] = None
    weight_val: Optional[float] = None
    try:
        height_val = parse_float_or_none(height_cm)
        weight_val = parse_float_or_none(weight_kg)
    except ValueError:
        errors.append("La altura y el peso deben ser valores numéricos.")

    if height_val is not None and not (100.0 <= height_val <= 250.0):
        errors.append("La altura (cm) debe estar entre 100 y 250.")
    if weight_val is not None and not (20.0 <= weight_val <= 300.0):
        errors.append("El peso (kg) debe estar entre 20 y 300.")

    if errors:
        # Re-render con valores enviados por el usuario
        return templates.TemplateResponse(
            "patients_edit.html",
            {
                "request": request,
                "patient_id": patient_id,
                "form_data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": date_of_birth,
                    "sex_at_birth": sex_value,  # mantener capitalizado
                    "email": email,
                    "phone": phone,
                    "height_cm": height_cm,
                    "weight_kg": weight_kg,
                    "consent_data_processing": consent_data_processing == "on",
                },
                "errors": errors,
            },
            status_code=400,
        )

    # --- Actualización del registro existente ---
    now = datetime.utcnow().isoformat() + "Z"

    patient["first_name"] = first_name_norm
    patient["last_name"]  = last_name_norm
    patient["date_of_birth"] = dob_obj.isoformat() if dob_obj else None
    patient["sex_at_birth"] = sex_value
    patient["email"] = email or None
    patient["phone"] = phone or None
    patient["consent_data_processing"] = True
    patient["updated_at"] = now

    # Altura / peso actuales
    patient["height_cm"] = height_val
    patient["weight_kg"] = weight_val

    # Recalcular IMC según los valores actuales
    if (height_val is not None) and (weight_val is not None):
        bmi_val = calculate_bmi(weight_val, height_val)
        patient["bmi_last"] = bmi_val
        patient["bmi_category_last"] = bmi_category(bmi_val)
        patient["bmi_last_measured_at"] = now
        patient["bmi_inputs_updated_at"] = now
    else:
        # Si falta alguno, dejamos IMC como no calculado
        patient["bmi_last"] = None
        patient["bmi_category_last"] = None
        patient["bmi_last_measured_at"] = None
        patient["bmi_inputs_updated_at"] = None

    # Conveniencias UI recalculadas
    patient["computed"] = {
        "display_name": f"{last_name_norm}, {first_name_norm}",
        "age_years": calculate_age_years(dob_obj) if dob_obj else None,
        "is_adult": (calculate_age_years(dob_obj) >= 18) if dob_obj else None,
        "contactable": bool((email and email.strip()) or (phone and phone.strip())),
    }

    # PRG: volver al listado
    return RedirectResponse(url="/patients", status_code=303)

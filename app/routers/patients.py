# app/routers/patients.py
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from typing import Any, Optional, Dict, List
from uuid import uuid4
from datetime import datetime, date

from pydantic import ValidationError
from app.models.patient import PatientCreate
from app.data.patients_seed import SEEDED_PATIENTS  # dict id->patient con computed/BMI

router = APIRouter(prefix="/patients", tags=["patients"])

# “BD” en memoria para el prototipo
PATIENTS: List[Dict[str, Any]] = []
_SEEDED = False


# ----------------------------- Helpers -----------------------------
def _errors_to_map(exc: ValidationError) -> Dict[str, List[str]]:
    """Convierte ValidationError a dict campo -> [mensajes] con traducción a español."""
    traducciones = {
        "String should have at least 1 character": "El texto debe tener al menos 1 carácter.",
        "String should have at most": "El texto es demasiado largo.",
        "Input should be a valid date or datetime": "Debe ingresar una fecha válida.",
        "Input should be a valid email address": "Debe ingresar un correo electrónico válido.",
        "Input should be a valid string": "Debe ingresar texto válido.",
        "Input should be a valid boolean": "Debe seleccionar un valor válido.",
        "Input should be": "Valor inválido. Debe seleccionar Masculino, Femenino u Otro.",
        "Value error, Debes aceptar el consentimiento para el tratamiento de datos.": 
            "Debes aceptar el consentimiento para el tratamiento de datos.",
    }

    out: Dict[str, List[str]] = {}
    for e in exc.errors():
        loc_tuple = e.get("loc", [])
        loc = str(loc_tuple[-1]) if loc_tuple else "non_field"
        msg = e.get("msg", "Valor inválido")

        # Buscar traducción exacta o parcial
        traducido = None
        if msg in traducciones:
            traducido = traducciones[msg]
        else:
            # búsqueda parcial (por ejemplo, 'Input should be')
            for key, val in traducciones.items():
                if msg.startswith(key):
                    traducido = val
                    break

        out.setdefault(loc, []).append(traducido or msg)
    return out


def _find_patient_index(pid: str) -> Optional[int]:
    return next((i for i, p in enumerate(PATIENTS) if p.get("patient_id") == pid), None)

def _float_or_none(s: Optional[str]) -> Optional[float]:
    """
    Convierte una cadena en float, o devuelve None si:
      - está vacía,
      - contiene espacios,
      - o no se puede convertir (por ejemplo 'abc').
    """
    if s is None:
        return None

    s = str(s).strip()
    if s == "":
        return None

    try:
        return float(s)
    except ValueError:
        # Si no es numérico, devolvemos None en lugar de lanzar excepción.
        return None


def _age_years(dob: Optional[date]) -> Optional[int]:
    if not dob:
        return None
    t = date.today()
    return max(0, t.year - dob.year - ((t.month, t.day) < (dob.month, dob.day)))

def _calc_bmi(weight_kg: float, height_cm: float) -> float:
    h = height_cm / 100.0
    return round(weight_kg / (h * h), 2)

def _bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "bajo peso"
    if bmi < 25.0:
        return "normal"
    if bmi < 30.0:
        return "sobrepeso"
    return "obesidad"

def _update_computed_and_bmi(rec: Dict[str, Any]) -> None:
    # computed
    dob_str = rec.get("date_of_birth")
    dob: Optional[date] = None
    try:
        if dob_str:
            y, m, d = map(int, dob_str.split("-"))
            dob = date(y, m, d)
    except Exception:
        dob = None

    rec.setdefault("computed", {})
    rec["computed"]["display_name"] = f"{rec.get('last_name','')}, {rec.get('first_name','')}".strip().strip(",")
    age = _age_years(dob)
    rec["computed"]["age_years"] = age
    rec["computed"]["is_adult"] = bool(age is not None and age >= 18)
    rec["computed"]["contactable"] = bool((rec.get("email") or "").strip() or (rec.get("phone") or "").strip())

    # BMI
    h, w = rec.get("height_cm"), rec.get("weight_kg")
    if isinstance(h, (int, float)) and isinstance(w, (int, float)) and h and w:
        bmi = _calc_bmi(w, h)
        now = datetime.utcnow().isoformat() + "Z"
        rec["bmi_last"] = bmi
        rec["bmi_category_last"] = _bmi_category(bmi)
        rec["bmi_last_measured_at"] = now
        rec["bmi_inputs_updated_at"] = now
    else:
        rec["bmi_last"] = None
        rec["bmi_category_last"] = None
        rec["bmi_last_measured_at"] = None
        rec["bmi_inputs_updated_at"] = None

def seed_patients_once() -> None:
    global _SEEDED, PATIENTS
    if _SEEDED or PATIENTS:
        return
    PATIENTS = list(SEEDED_PATIENTS.values())  # seed ya trae computed/BMI
    _SEEDED = True


# ----------------------------- Rutas -----------------------------
@router.get("")
async def list_patients(request: Request):
    seed_patients_once()
    patients_sorted = sorted(PATIENTS, key=lambda p: (p.get("last_name",""), p.get("first_name","")))
    return request.app.state.templates.TemplateResponse(
        "patients_list.html",
        {"request": request, "patients": patients_sorted}
    )


@router.get("/create")
async def get_create_patient(request: Request):
    return request.app.state.templates.TemplateResponse(
        "patients_create.html",
        {"request": request, "form_data": {}, "errors": {}, "errors_list": []}
    )


@router.post("/create")
async def post_create_patient(
    request: Request,
    # ⚠️ Todos opcionales para evitar 422 de FastAPI y manejar Pydantic nosotros:
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),     # YYYY-MM-DD
    sex_at_birth: Optional[str] = Form(None),      # ES -> EN para validar
    gender_identity: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    height_cm: Optional[str] = Form(None),
    weight_kg: Optional[str] = Form(None),
    consent_data_processing: Optional[str] = Form(None),  # "on" si marcado
):
    form_for_validation = {
        "first_name": (first_name or "").strip(),
        "last_name":  (last_name  or "").strip(),
        "date_of_birth": (date_of_birth or "").strip(),
        "sex_at_birth": (sex_at_birth or "").strip(),
        "gender_identity": (gender_identity or "").strip() or None,
        "email": (email or "").strip() or None,
        "phone": (phone or "").strip() or None,
        "notes": (notes or "").strip() or None,
        "consent_data_processing": (consent_data_processing == "on"),
    }

    errors_map: Dict[str, List[str]] = {}
    clean: Optional[PatientCreate] = None
    try:
        clean = PatientCreate.model_validate(form_for_validation)  # ✅ Pydantic
    except ValidationError as ve:
        errors_map = _errors_to_map(ve)

    # Política de consentimiento
    if not form_for_validation["consent_data_processing"]:
        errors_map.setdefault("consent_data_processing", []).append(
            "Debes aceptar el consentimiento para el tratamiento de datos."
        )

    if errors_map:
        form_back = dict(form_for_validation)
        form_back["sex_at_birth"] = sex_at_birth or ""
        form_back["height_cm"] = height_cm
        form_back["weight_kg"] = weight_kg
        return request.app.state.templates.TemplateResponse(
            "patients_create.html",
            {"request": request, "form_data": form_back, "errors": errors_map,
             "errors_list": [msg for v in errors_map.values() for msg in v]},
            status_code=400
        )

    # A partir de aquí, clean está garantizado por el early return anterior
    assert clean is not None

    now = datetime.utcnow().isoformat() + "Z"
    rec: Dict[str, Any] = clean.model_dump()
    rec.update({
        "patient_id": str(uuid4()),
        "created_at": now,
        "updated_at": now,
        "sex_at_birth": sex_at_birth or "",   # mantener ES para la UI
        "height_cm": _float_or_none(height_cm),
        "weight_kg": _float_or_none(weight_kg),
    })

    _update_computed_and_bmi(rec)
    PATIENTS.append(rec)
    return RedirectResponse(url="/patients", status_code=303)


@router.get("/{patient_id}/edit")
async def get_edit_patient(request: Request, patient_id: str):
    seed_patients_once()
    idx = _find_patient_index(patient_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    p = PATIENTS[idx]
    form_data = {
        "first_name": p.get("first_name",""),
        "last_name": p.get("last_name",""),
        "date_of_birth": p.get("date_of_birth",""),
        "sex_at_birth": p.get("sex_at_birth",""),  # ES
        "gender_identity": p.get("gender_identity") or "",
        "email": p.get("email") or "",
        "phone": p.get("phone") or "",
        "notes": p.get("notes") or "",
        "height_cm": "" if p.get("height_cm") is None else p["height_cm"],
        "weight_kg": "" if p.get("weight_kg") is None else p["weight_kg"],
        "consent_data_processing": bool(p.get("consent_data_processing", True)),
    }
    return request.app.state.templates.TemplateResponse(
        "patients_edit.html",
        {"request": request, "patient_id": patient_id, "form_data": form_data,
         "errors": {}, "errors_list": []}
    )


@router.post("/{patient_id}/edit")
async def post_edit_patient(
    request: Request,
    patient_id: str,
    # ⚠️ Opcionales para evitar 422 y manejar Pydantic
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    date_of_birth: Optional[str] = Form(None),
    sex_at_birth: Optional[str] = Form(None),      # ES -> EN para validar
    gender_identity: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    height_cm: Optional[str] = Form(None),
    weight_kg: Optional[str] = Form(None),
    consent_data_processing: Optional[str] = Form(None),
):
    idx = _find_patient_index(patient_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    form_for_validation = {
        "first_name": (first_name or "").strip(),
        "last_name":  (last_name  or "").strip(),
        "date_of_birth": (date_of_birth or "").strip(),
        "sex_at_birth": (sex_at_birth or "").strip(),
        "gender_identity": (gender_identity or "").strip() or None,
        "email": (email or "").strip() or None,
        "phone": (phone or "").strip() or None,
        "notes": (notes or "").strip() or None,
        "consent_data_processing": (consent_data_processing == "on")
            if consent_data_processing is not None
            else bool(PATIENTS[idx].get("consent_data_processing", True)),
    }

    errors_map: Dict[str, List[str]] = {}
    clean: Optional[PatientCreate] = None
    try:
        clean = PatientCreate.model_validate(form_for_validation)  # ✅ Pydantic
    except ValidationError as ve:
        errors_map = _errors_to_map(ve)

    if not form_for_validation["consent_data_processing"]:
        errors_map.setdefault("consent_data_processing", []).append(
            "Debes aceptar el consentimiento para el tratamiento de datos."
        )

    if errors_map:
        form_back = dict(form_for_validation)
        form_back["sex_at_birth"] = sex_at_birth or ""  # ES para UI
        form_back["height_cm"] = height_cm
        form_back["weight_kg"] = weight_kg
        return request.app.state.templates.TemplateResponse(
            "patients_edit.html",
            {"request": request, "patient_id": patient_id, "form_data": form_back,
             "errors": errors_map, "errors_list": [msg for v in errors_map.values() for msg in v]},
            status_code=400
        )

    assert clean is not None

    now = datetime.utcnow().isoformat() + "Z"
    rec = PATIENTS[idx]
    rec.update(clean.model_dump())
    rec.update({
        "sex_at_birth": sex_at_birth or "",  # ES para UI
        "height_cm": _float_or_none(height_cm),
        "weight_kg": _float_or_none(weight_kg),
        "updated_at": now,
    })
    _update_computed_and_bmi(rec)

    return RedirectResponse(url="/patients", status_code=303)


@router.post("/{patient_id}/delete")
async def delete_patient(request: Request, patient_id: str):
    idx = _find_patient_index(patient_id)
    if idx is not None:
        PATIENTS.pop(idx)
    return RedirectResponse(url="/patients", status_code=303)

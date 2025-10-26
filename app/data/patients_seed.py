# ============================================
# 📦 Datos semilla: pacientes ficticios (didáctico)
# ============================================
# Nota: Valores "computed" (edad, etc.) están fijos a efectos didácticos.
# En versiones posteriores podemos recalcularlos al arrancar si se desea.

from typing import Dict, Any

SEEDED_PATIENTS: Dict[str, Dict[str, Any]] = {
    # Paciente 1: IMC normal
    "f0b5a2e1-1a9d-4c6b-9e11-aaa111aaa111": {
        "patient_id": "f0b5a2e1-1a9d-4c6b-9e11-aaa111aaa111",
        "first_name": "Laura",
        "last_name": "Gómez",
        "date_of_birth": "1992-04-15",
        "sex_at_birth": "Femenino",
        "email": "laura.gomez@example.com",
        "phone": "+34 600 112 233",
        "consent_data_processing": True,
        "created_at": "2025-10-26T10:00:00Z",
        "updated_at": "2025-10-26T10:00:00Z",
        "height_cm": 165.0,
        "weight_kg": 60.0,
        "bmi_inputs_updated_at": "2025-10-26T10:00:00Z",
        "bmi_last": 22.04,
        "bmi_category_last": "normal",
        "bmi_last_measured_at": "2025-10-26T10:00:00Z",
        "computed": {
            "display_name": "Gómez, Laura",
            "age_years": 33,
            "is_adult": True,
            "contactable": True,
        },
    },

    # Paciente 2: sobrepeso
    "a8f1c3b2-4e0a-4f9b-9b77-bbb222bbb222": {
        "patient_id": "a8f1c3b2-4e0a-4f9b-9b77-bbb222bbb222",
        "first_name": "Carlos",
        "last_name": "López",
        "date_of_birth": "1988-09-10",
        "sex_at_birth": "Masculino  ",
        "email": "carlos.lopez@example.com",
        "phone": "+34 611 223 344",
        "consent_data_processing": True,
        "created_at": "2025-10-26T10:05:00Z",
        "updated_at": "2025-10-26T10:05:00Z",
        "height_cm": 178.0,
        "weight_kg": 92.0,
        "bmi_inputs_updated_at": "2025-10-26T10:05:00Z",
        "bmi_last": 29.04,
        "bmi_category_last": "sobrepeso",
        "bmi_last_measured_at": "2025-10-26T10:05:00Z",
        "computed": {
            "display_name": "López, Carlos",
            "age_years": 37,
            "is_adult": True,
            "contactable": True,
        },
    },
}

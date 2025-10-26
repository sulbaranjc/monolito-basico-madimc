# app/data/patients_seed.py
# Seed con la MISMA forma que espera tu UI (computed + BMI opcional)

SEEDED_PATIENTS = {
    "seed-1": {
        "patient_id": "seed-1",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1988-05-21",
        "sex_at_birth": "Masculino",
        "email": "john.doe@example.com",
        "phone": "+34 600 111 111",
        "consent_data_processing": True,
        "height_cm": 174.0,
        "weight_kg": 82.5,
        "bmi_inputs_updated_at": "2025-10-01T10:00:00Z",
        "bmi_last": 27.24,
        "bmi_category_last": "sobrepeso",
        "bmi_last_measured_at": "2025-10-01T10:00:00Z",
        "computed": {
            "display_name": "Doe, John",
            "age_years": 37,          # aprox; es seed educativo
            "is_adult": True,
            "contactable": True
        },
        "created_at": "2025-10-01T10:00:00Z",
        "updated_at": "2025-10-01T10:00:00Z"
    },
    "seed-2": {
        "patient_id": "seed-2",
        "first_name": "María",
        "last_name": "Pérez",
        "date_of_birth": "1993-11-02",
        "sex_at_birth": "Femenino",
        "email": "maria.perez@example.com",
        "phone": "+34 600 222 222",
        "consent_data_processing": True,
        "height_cm": 165.0,
        "weight_kg": 61.0,
        "bmi_inputs_updated_at": "2025-10-01T11:00:00Z",
        "bmi_last": 22.40,
        "bmi_category_last": "normal",
        "bmi_last_measured_at": "2025-10-01T11:00:00Z",
        "computed": {
            "display_name": "Pérez, María",
            "age_years": 31,
            "is_adult": True,
            "contactable": True
        },
        "created_at": "2025-10-01T11:00:00Z",
        "updated_at": "2025-10-01T11:00:00Z"
    },
    "seed-3": {
        "patient_id": "seed-3",
        "first_name": "Alex",
        "last_name": "Kim",
        "date_of_birth": "2001-03-14",
        "sex_at_birth": "Otro",
        "email": None,
        "phone": None,
        "consent_data_processing": True,
        "height_cm": None,
        "weight_kg": None,
        "bmi_inputs_updated_at": None,
        "bmi_last": None,
        "bmi_category_last": None,
        "bmi_last_measured_at": None,
        "computed": {
            "display_name": "Kim, Alex",
            "age_years": 24,
            "is_adult": True,
            "contactable": False
        },
        "created_at": "2025-10-01T12:00:00Z",
        "updated_at": "2025-10-01T12:00:00Z"
    }
}

# app/models/patient.py
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional, Literal

SexAtBirth = Literal["male", "female", "other"]

class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=60)
    last_name: str  = Field(..., min_length=1, max_length=60)
    date_of_birth: date
    sex_at_birth: SexAtBirth
    gender_identity: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^[0-9+\-() ]{7,20}$")
    notes: Optional[str] = Field(None, max_length=500)
    consent_data_processing: bool = True

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=60)
    last_name: Optional[str]  = Field(None, min_length=1, max_length=60)
    date_of_birth: Optional[date] = None
    sex_at_birth: Optional[SexAtBirth] = None
    gender_identity: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^[0-9+\-() ]{7,20}$")
    notes: Optional[str] = Field(None, max_length=500)
    consent_data_processing: Optional[bool] = None

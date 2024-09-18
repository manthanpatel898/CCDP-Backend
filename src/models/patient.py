# src/models/patient.py
from dataclasses import dataclass, field

@dataclass
class Patient:
    first_name: str
    last_name: str
    email: str
    age: int
    weight: float
    height: float
    address: str
    mobile_number: str
    patient_code: str = field(default_factory=str)
    onboarding_info: dict = field(default_factory=dict)

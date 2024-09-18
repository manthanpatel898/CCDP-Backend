import random
import string

def generate_patient_code():
    return ''.join(random.choices(string.digits, k=6))

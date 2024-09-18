# src/services/otp_service.py
import random
import time

# In-memory storage for OTPs (use Redis or database in production)
otp_storage = {}

def send_otp(mobile_number):
    otp = random.randint(100000, 999999)
    otp_storage[mobile_number] = {
        'otp': otp,
        'timestamp': time.time()
    }
    # TODO: Integrate with an SMS gateway to send the OTP
    print(f"Sending OTP {otp} to mobile number {mobile_number}")  # For testing
    return True

def verify_otp(mobile_number, otp_input):
    otp_data = otp_storage.get(mobile_number)
    if not otp_data:
        return False
    if time.time() - otp_data['timestamp'] > 600:  # OTP valid for 10 minutes
        del otp_storage[mobile_number]
        return False
    if otp_data['otp'] == otp_input:
        del otp_storage[mobile_number]
        return True
    return False

import smtplib
from email.mime.text import MIMEText
from ..config import Config

def send_patient_code(email, patient_code):
    msg = MIMEText(f"Your patient code is: {patient_code}")
    msg['Subject'] = 'Your Patient Code'
    msg['From'] = 'ahmed.mekallach@gmail.com'
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('ahmed.mekallach@gmail.com', 'txuncmsrwrinacfj')
        server.send_message(msg)

import qrcode
import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import EMAIL_USER, EMAIL_PASS, SMTP_SERVER, SMTP_PORT

def generate_qr(data):
    qr = qrcode.make(data)
    qr_path = f"static/qrs/{data}.png"
    qr.save(qr_path)
    return qr_path

def decode_qr(image):
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    return data

def send_email(to_email, qr_path):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = "Tu código QR para el Coworking"

    body = "Aquí está tu código QR para acceder al coworking."
    msg.attach(MIMEText(body, "plain"))

    with open(qr_path, "rb") as attachment:
        msg.attach(MIMEText(attachment.read(), "base64", "utf-8"))
        msg.get_payload()[-1]["Content-Disposition"] = f'attachment; filename="{qr_path}"'

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, to_email, msg.as_string())
    server.quit()

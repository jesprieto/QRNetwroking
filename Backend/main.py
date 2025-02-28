from flask import Flask, request, jsonify, send_file
import qrcode
import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from utils import generate_qr, decode_qr, send_email

app = Flask(__name__)

@app.route("/generate_qr", methods=["POST"])
def generate_qr_route():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    qr_path = generate_qr(email)
    send_email(email, qr_path)

    return jsonify({"message": "QR Code generated and sent"}), 200

@app.route("/validate_qr", methods=["POST"])
def validate_qr_route():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No QR code uploaded"}), 400

    image_np = np.fromstring(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    qr_data = decode_qr(image)

    if qr_data:
        return jsonify({"message": "QR Code Valid", "data": qr_data}), 200
    else:
        return jsonify({"message": "Invalid QR Code"}), 400

if __name__ == "__main__":
    app.run(debug=True)
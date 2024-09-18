# src/controllers/patient_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from bson.objectid import ObjectId
from ..db import mongo
from ..services.otp_service import send_otp, verify_otp
from ..services.auth_service import generate_patient_code

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/patient')

@patient_bp.route('/request_otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    mobile_number = data.get('mobile_number')
    if not mobile_number:
        return jsonify({'error': 'Mobile number is required'}), 400
    # Send OTP to the mobile number
    send_otp(mobile_number)
    return jsonify({'message': 'OTP sent to mobile number'}), 200

@patient_bp.route('/verify_otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    mobile_number = data.get('mobile_number')
    otp_input = data.get('otp')
    if not mobile_number or not otp_input:
        return jsonify({'error': 'Mobile number and OTP are required'}), 400
    if verify_otp(mobile_number, int(otp_input)):
        # Create a temporary access token for the patient to enter patient code
        access_token = create_access_token(identity={'mobile_number': mobile_number})
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid or expired OTP'}), 401

@patient_bp.route('/verify_patient_code', methods=['POST'])
@jwt_required()
def verify_patient_code():
    current_user = get_jwt_identity()
    mobile_number = current_user.get('mobile_number')
    data = request.get_json()
    patient_code = data.get('patient_code')
    if not patient_code:
        return jsonify({'error': 'Patient code is required'}), 400
    # Find patient by patient_code and mobile_number
    patient = mongo.db.patients.find_one({'patient_code': patient_code, 'mobile_number': mobile_number})
    if patient:
        # Create a new access token with patient ID
        access_token = create_access_token(identity=str(patient['_id']))
        return jsonify({'access_token': access_token, 'message': 'Patient profile verified'}), 200
    else:
        return jsonify({'error': 'Invalid patient code or mobile number'}), 401

@patient_bp.route('/onboarding', methods=['POST'])
@jwt_required()
def onboarding():
    patient_id = get_jwt_identity()
    data = request.get_json()
    # Update patient onboarding info
    mongo.db.patients.update_one({'_id': ObjectId(patient_id)}, {'$set': {'onboarding_info': data}})
    return jsonify({'message': 'Onboarding completed'}), 200

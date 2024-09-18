# src/controllers/admin_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt, create_access_token
)
from functools import wraps
from ..db import mongo
from ..services.auth_service import generate_patient_code
from ..services.email_service import send_patient_code
from ..models.admin import Admin  # Import the Admin model

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')
print('test')

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admins only!'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Check if admin already exists
    if mongo.db.admins.find_one({'email': email}):
        return jsonify({'error': 'Admin with this email already exists'}), 400

    # Hash the password and store the admin
    admin_data = Admin.create_admin(email, password)
    mongo.db.admins.insert_one(admin_data)

    return jsonify({'message': 'Admin registered successfully'}), 201

@admin_bp.route('/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    admin = mongo.db.admins.find_one({'email': email})
    if not admin:
        return jsonify({'error': 'Invalid email or password'}), 401

    if not Admin.verify_password(password, admin['password_hash']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create access token with admin role using additional_claims
    access_token = create_access_token(
        identity=str(admin['_id']),
        additional_claims={'role': 'admin'}
    )

    return jsonify({'access_token': access_token}), 200

@admin_bp.route('/register_patient', methods=['POST'])
@admin_required
def register_patient():
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'email', 'age', 'weight', 'height', 'address', 'mobile_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Generate unique 6-digit patient code
    patient_code = generate_patient_code()
    data['patient_code'] = patient_code

    # Insert patient data into the database
    mongo.db.patients.insert_one(data)

    # Send patient code via email (implement this function accordingly)
    send_patient_code(data['email'], patient_code)

    return jsonify({'message': 'Patient registered successfully'}), 201

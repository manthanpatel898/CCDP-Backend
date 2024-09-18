from flask import Flask
from flask_jwt_extended import JWTManager
from .config import Config
from .db import init_db

def create_app():
    print('asd')
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    JWTManager(app)

    # Register Blueprints
    from .controllers.patient_controller import patient_bp
    # from .controllers.doctor_controller import doctor_bp
    from .controllers.admin_controller import admin_bp

    app.register_blueprint(patient_bp)
    # app.register_blueprint(doctor_bp)
    app.register_blueprint(admin_bp)

    return app



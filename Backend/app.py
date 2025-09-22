from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER', 'fra_user')}:{os.getenv('POSTGRES_PASSWORD', 'fra_password')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'fra_db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Import models
from api.models import User, Claim, Asset, Scheme

# Import blueprints
from api.auth import auth_bp
from api.claims import claims_bp
from api.assets import assets_bp
from api.dss import dss_bp
from api.ocr import ocr_bp
from api.satellite import satellite_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(claims_bp, url_prefix='/api/claims')
app.register_blueprint(assets_bp, url_prefix='/api/assets')
app.register_blueprint(dss_bp, url_prefix='/api/dss')
app.register_blueprint(ocr_bp, url_prefix='/api/ocr')
app.register_blueprint(satellite_bp, url_prefix='/api/satellite')

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'FRA WebGIS DSS API is running',
        'version': '1.0.0'
    })

@app.route('/api/docs')
def api_docs():
    return jsonify({
        'title': 'FRA WebGIS DSS API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'claims': '/api/claims',
            'assets': '/api/assets',
            'dss': '/api/dss',
            'ocr': '/api/ocr',
            'satellite': '/api/satellite'
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

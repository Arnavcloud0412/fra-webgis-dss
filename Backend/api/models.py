from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # user, admin, officer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claims = db.relationship('Claim', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Claim(db.Model):
    __tablename__ = 'claims'
    
    id = db.Column(db.Integer, primary_key=True)
    claim_number = db.Column(db.String(50), unique=True, nullable=False)
    applicant_name = db.Column(db.String(100), nullable=False)
    applicant_address = db.Column(db.Text)
    village = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    claim_type = db.Column(db.String(50))  # individual, community
    land_area = db.Column(db.Float)  # in hectares
    land_description = db.Column(db.Text)
    supporting_documents = db.Column(db.Text)  # JSON array of document paths
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    geometry = db.Column(Geometry('POLYGON', srid=4326))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    assets = db.relationship('Asset', backref='claim', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'claim_number': self.claim_number,
            'applicant_name': self.applicant_name,
            'applicant_address': self.applicant_address,
            'village': self.village,
            'district': self.district,
            'state': self.state,
            'claim_type': self.claim_type,
            'land_area': self.land_area,
            'land_description': self.land_description,
            'supporting_documents': json.loads(self.supporting_documents) if self.supporting_documents else [],
            'status': self.status,
            'geometry': self.geometry.wkt if self.geometry else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50))  # forest, agricultural, residential
    area_hectares = db.Column(db.Float)
    description = db.Column(db.Text)
    satellite_image_path = db.Column(db.String(200))
    classification_result = db.Column(db.Text)  # JSON with ML classification results
    confidence_score = db.Column(db.Float)
    geometry = db.Column(Geometry('POLYGON', srid=4326))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_name': self.asset_name,
            'asset_type': self.asset_type,
            'area_hectares': self.area_hectares,
            'description': self.description,
            'satellite_image_path': self.satellite_image_path,
            'classification_result': json.loads(self.classification_result) if self.classification_result else {},
            'confidence_score': self.confidence_score,
            'geometry': self.geometry.wkt if self.geometry else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Scheme(db.Model):
    __tablename__ = 'schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(100), nullable=False)
    scheme_code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text)  # JSON with criteria
    benefits = db.Column(db.Text)  # JSON with benefits
    application_process = db.Column(db.Text)
    contact_info = db.Column(db.Text)  # JSON with contact details
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'scheme_name': self.scheme_name,
            'scheme_code': self.scheme_code,
            'description': self.description,
            'eligibility_criteria': json.loads(self.eligibility_criteria) if self.eligibility_criteria else {},
            'benefits': json.loads(self.benefits) if self.benefits else {},
            'application_process': self.application_process,
            'contact_info': json.loads(self.contact_info) if self.contact_info else {},
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

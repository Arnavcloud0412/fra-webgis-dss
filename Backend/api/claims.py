from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Claim, User, db
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
import json

claims_bp = Blueprint('claims', __name__)

@claims_bp.route('/', methods=['GET'])
@jwt_required()
def get_claims():
    """Get all claims for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Admin can see all claims, others see only their own
        if user.role == 'admin':
            claims = Claim.query.all()
        else:
            claims = Claim.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'claims': [claim.to_dict() for claim in claims]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@claims_bp.route('/', methods=['POST'])
@jwt_required()
def create_claim():
    """Create a new claim"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['applicant_name', 'village', 'district', 'state', 'claim_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Generate claim number
        claim_count = Claim.query.count()
        claim_number = f"FRA{claim_count + 1:06d}"
        
        # Create claim
        claim = Claim(
            claim_number=claim_number,
            applicant_name=data['applicant_name'],
            applicant_address=data.get('applicant_address'),
            village=data['village'],
            district=data['district'],
            state=data['state'],
            claim_type=data['claim_type'],
            land_area=data.get('land_area'),
            land_description=data.get('land_description'),
            supporting_documents=json.dumps(data.get('supporting_documents', [])),
            user_id=user_id
        )
        
        # Handle geometry if provided
        if data.get('geometry'):
            try:
                geom = shape(data['geometry'])
                claim.geometry = from_shape(geom, srid=4326)
            except Exception as e:
                return jsonify({'error': f'Invalid geometry: {str(e)}'}), 400
        
        db.session.add(claim)
        db.session.commit()
        
        return jsonify({
            'message': 'Claim created successfully',
            'claim': claim.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@claims_bp.route('/<int:claim_id>', methods=['GET'])
@jwt_required()
def get_claim(claim_id):
    """Get a specific claim"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        claim = Claim.query.get(claim_id)
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'claim': claim.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@claims_bp.route('/<int:claim_id>', methods=['PUT'])
@jwt_required()
def update_claim(claim_id):
    """Update a specific claim"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        claim = Claim.query.get(claim_id)
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = [
            'applicant_name', 'applicant_address', 'village', 'district', 'state',
            'claim_type', 'land_area', 'land_description', 'supporting_documents'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'supporting_documents':
                    claim.supporting_documents = json.dumps(data[field])
                else:
                    setattr(claim, field, data[field])
        
        # Handle geometry update
        if 'geometry' in data:
            try:
                geom = shape(data['geometry'])
                claim.geometry = from_shape(geom, srid=4326)
            except Exception as e:
                return jsonify({'error': f'Invalid geometry: {str(e)}'}), 400
        
        # Only admin can update status
        if 'status' in data and user.role == 'admin':
            claim.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Claim updated successfully',
            'claim': claim.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@claims_bp.route('/<int:claim_id>', methods=['DELETE'])
@jwt_required()
def delete_claim(claim_id):
    """Delete a specific claim"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        claim = Claim.query.get(claim_id)
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(claim)
        db.session.commit()
        
        return jsonify({'message': 'Claim deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

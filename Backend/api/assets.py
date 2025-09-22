from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Asset, Claim, User, db
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
import json

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/', methods=['GET'])
@jwt_required()
def get_assets():
    """Get all assets for the current user's claims"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Admin can see all assets, others see only their own
        if user.role == 'admin':
            assets = Asset.query.all()
        else:
            # Get user's claims first
            user_claims = Claim.query.filter_by(user_id=user_id).all()
            claim_ids = [claim.id for claim in user_claims]
            assets = Asset.query.filter(Asset.claim_id.in_(claim_ids)).all()
        
        return jsonify({
            'assets': [asset.to_dict() for asset in assets]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/', methods=['POST'])
@jwt_required()
def create_asset():
    """Create a new asset"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('asset_name') or not data.get('claim_id'):
            return jsonify({'error': 'Asset name and claim_id are required'}), 400
        
        # Check if claim belongs to user
        claim = Claim.query.get(data['claim_id'])
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404
        
        user = User.query.get(user_id)
        if user.role != 'admin' and claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Create asset
        asset = Asset(
            asset_name=data['asset_name'],
            asset_type=data.get('asset_type'),
            area_hectares=data.get('area_hectares'),
            description=data.get('description'),
            satellite_image_path=data.get('satellite_image_path'),
            classification_result=json.dumps(data.get('classification_result', {})),
            confidence_score=data.get('confidence_score'),
            claim_id=data['claim_id']
        )
        
        # Handle geometry if provided
        if data.get('geometry'):
            try:
                geom = shape(data['geometry'])
                asset.geometry = from_shape(geom, srid=4326)
            except Exception as e:
                return jsonify({'error': f'Invalid geometry: {str(e)}'}), 400
        
        db.session.add(asset)
        db.session.commit()
        
        return jsonify({
            'message': 'Asset created successfully',
            'asset': asset.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    """Get a specific asset"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and asset.claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'asset': asset.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['PUT'])
@jwt_required()
def update_asset(asset_id):
    """Update a specific asset"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and asset.claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = [
            'asset_name', 'asset_type', 'area_hectares', 'description',
            'satellite_image_path', 'classification_result', 'confidence_score'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'classification_result':
                    asset.classification_result = json.dumps(data[field])
                else:
                    setattr(asset, field, data[field])
        
        # Handle geometry update
        if 'geometry' in data:
            try:
                geom = shape(data['geometry'])
                asset.geometry = from_shape(geom, srid=4326)
            except Exception as e:
                return jsonify({'error': f'Invalid geometry: {str(e)}'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Asset updated successfully',
            'asset': asset.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/<int:asset_id>', methods=['DELETE'])
@jwt_required()
def delete_asset(asset_id):
    """Delete a specific asset"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and asset.claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(asset)
        db.session.commit()
        
        return jsonify({'message': 'Asset deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@assets_bp.route('/by-claim/<int:claim_id>', methods=['GET'])
@jwt_required()
def get_assets_by_claim(claim_id):
    """Get all assets for a specific claim"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        claim = Claim.query.get(claim_id)
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404
        
        # Check permissions
        if user.role != 'admin' and claim.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        assets = Asset.query.filter_by(claim_id=claim_id).all()
        
        return jsonify({
            'claim_id': claim_id,
            'assets': [asset.to_dict() for asset in assets]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

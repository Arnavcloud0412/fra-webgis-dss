import json
import os
from typing import Dict, List, Any, Tuple
from flask import Blueprint, request, jsonify
from api.models import Claim, Scheme, db
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

dss_bp = Blueprint('dss', __name__)

class RuleEngine:
    """Rule-based decision support system"""
    
    def __init__(self):
        self.rules = self._load_rules()
    
    def _load_rules(self) -> List[Dict]:
        """Load decision rules from file"""
        rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
        try:
            with open(rules_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_rules()
    
    def _get_default_rules(self) -> List[Dict]:
        """Get default rules for FRA scheme matching"""
        return [
            {
                "id": "rule_001",
                "name": "Individual Forest Rights",
                "description": "Match individual forest rights claimants to forest development schemes",
                "conditions": {
                    "claim_type": "individual",
                    "land_area": {"min": 0.1, "max": 4.0},
                    "land_type": "forest"
                },
                "schemes": ["forest_development", "livelihood_support"],
                "priority": "high",
                "weight": 0.9
            },
            {
                "id": "rule_002",
                "name": "Community Forest Rights",
                "description": "Match community forest rights claimants to community development schemes",
                "conditions": {
                    "claim_type": "community",
                    "land_area": {"min": 1.0, "max": 1000.0},
                    "land_type": "forest"
                },
                "schemes": ["community_forest_management", "ecotourism", "forest_protection"],
                "priority": "high",
                "weight": 0.95
            },
            {
                "id": "rule_003",
                "name": "Agricultural Land Rights",
                "description": "Match agricultural land claimants to agricultural schemes",
                "conditions": {
                    "land_type": "agricultural",
                    "land_area": {"min": 0.5, "max": 10.0}
                },
                "schemes": ["agricultural_support", "irrigation", "crop_insurance"],
                "priority": "medium",
                "weight": 0.8
            },
            {
                "id": "rule_004",
                "name": "Small Landholders",
                "description": "Match small landholders to micro-finance and skill development schemes",
                "conditions": {
                    "land_area": {"max": 1.0},
                    "income_level": "low"
                },
                "schemes": ["micro_finance", "skill_development", "women_empowerment"],
                "priority": "medium",
                "weight": 0.7
            },
            {
                "id": "rule_005",
                "name": "Tribal Communities",
                "description": "Match tribal communities to tribal development schemes",
                "conditions": {
                    "community_type": "tribal",
                    "claim_type": "community"
                },
                "schemes": ["tribal_development", "cultural_preservation", "education_support"],
                "priority": "high",
                "weight": 0.9
            }
        ]
    
    def evaluate_claim(self, claim_data: Dict) -> List[Dict]:
        """Evaluate claim against rules and return matching schemes"""
        matches = []
        
        for rule in self.rules:
            if self._check_conditions(claim_data, rule['conditions']):
                match_score = self._calculate_match_score(claim_data, rule)
                
                matches.append({
                    'rule_id': rule['id'],
                    'rule_name': rule['name'],
                    'description': rule['description'],
                    'schemes': rule['schemes'],
                    'priority': rule['priority'],
                    'match_score': match_score,
                    'weight': rule['weight']
                })
        
        # Sort by match score and priority
        matches.sort(key=lambda x: (x['match_score'], x['weight']), reverse=True)
        
        return matches
    
    def _check_conditions(self, claim_data: Dict, conditions: Dict) -> bool:
        """Check if claim data meets rule conditions"""
        for condition, value in conditions.items():
            if condition not in claim_data:
                return False
            
            claim_value = claim_data[condition]
            
            if isinstance(value, dict):
                if 'min' in value and claim_value < value['min']:
                    return False
                if 'max' in value and claim_value > value['max']:
                    return False
            elif isinstance(value, list):
                if claim_value not in value:
                    return False
            else:
                if claim_value != value:
                    return False
        
        return True
    
    def _calculate_match_score(self, claim_data: Dict, rule: Dict) -> float:
        """Calculate match score for a rule"""
        base_score = rule['weight']
        
        # Adjust score based on land area
        if 'land_area' in claim_data:
            land_area = claim_data['land_area']
            if land_area and land_area > 0:
                # Normalize land area score
                area_score = min(land_area / 10.0, 1.0)  # Cap at 1.0
                base_score += area_score * 0.1
        
        # Adjust score based on claim completeness
        completeness_score = self._calculate_completeness_score(claim_data)
        base_score += completeness_score * 0.2
        
        return min(base_score, 1.0)  # Cap at 1.0
    
    def _calculate_completeness_score(self, claim_data: Dict) -> float:
        """Calculate completeness score for claim data"""
        required_fields = ['applicant_name', 'village', 'district', 'state', 'claim_type']
        filled_fields = sum(1 for field in required_fields if claim_data.get(field))
        
        return filled_fields / len(required_fields)

class MLDSS:
    """Machine Learning-based Decision Support System"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_names = [
            'land_area', 'claim_type_encoded', 'village_population',
            'district_development_index', 'state_gdp_per_capita',
            'distance_to_forest', 'soil_quality', 'water_availability'
        ]
    
    def prepare_training_data(self, claims: List[Dict], scheme_matches: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for ML model"""
        features = []
        labels = []
        
        for claim, matches in zip(claims, scheme_matches):
            # Extract features
            feature_vector = self._extract_features(claim)
            features.append(feature_vector)
            
            # Extract label (most relevant scheme)
            if matches:
                best_match = matches[0]
                labels.append(best_match['schemes'][0])  # Use first scheme as label
            else:
                labels.append('no_match')
        
        return np.array(features), np.array(labels)
    
    def _extract_features(self, claim_data: Dict) -> List[float]:
        """Extract features from claim data"""
        features = []
        
        # Land area
        features.append(claim_data.get('land_area', 0.0))
        
        # Claim type (encoded)
        claim_type = claim_data.get('claim_type', 'individual')
        claim_type_encoded = 1 if claim_type == 'community' else 0
        features.append(claim_type_encoded)
        
        # Mock additional features (in production, these would come from external data)
        features.append(np.random.uniform(100, 10000))  # Village population
        features.append(np.random.uniform(0.1, 1.0))    # District development index
        features.append(np.random.uniform(50000, 200000))  # State GDP per capita
        features.append(np.random.uniform(0, 50))        # Distance to forest (km)
        features.append(np.random.uniform(0.1, 1.0))     # Soil quality
        features.append(np.random.uniform(0.1, 1.0))     # Water availability
        
        return features
    
    def train_model(self, claims: List[Dict], scheme_matches: List[Dict]) -> Dict[str, Any]:
        """Train ML model for scheme matching"""
        try:
            # Prepare data
            X, y = self.prepare_training_data(claims, scheme_matches)
            
            # Encode labels
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X, y_encoded)
            
            # Evaluate
            train_score = self.model.score(X, y_encoded)
            
            # Save model
            model_path = os.path.join(os.path.dirname(__file__), 'dss_model.joblib')
            joblib.dump({
                'model': self.model,
                'label_encoder': self.label_encoder,
                'feature_names': self.feature_names
            }, model_path)
            
            return {
                'accuracy': train_score,
                'model_path': model_path,
                'feature_importance': self.model.feature_importances_.tolist(),
                'classes': self.label_encoder.classes_.tolist()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def predict_schemes(self, claim_data: Dict) -> Dict[str, Any]:
        """Predict schemes for a claim using ML model"""
        try:
            if not self.model:
                # Load model
                model_path = os.path.join(os.path.dirname(__file__), 'dss_model.joblib')
                if os.path.exists(model_path):
                    model_data = joblib.load(model_path)
                    self.model = model_data['model']
                    self.label_encoder = model_data['label_encoder']
                else:
                    return {'error': 'Model not trained yet'}
            
            # Extract features
            features = np.array([self._extract_features(claim_data)])
            
            # Predict
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Get scheme name
            scheme_name = self.label_encoder.inverse_transform([prediction])[0]
            
            # Get top 3 predictions
            top_indices = np.argsort(probabilities)[-3:][::-1]
            top_schemes = []
            for idx in top_indices:
                scheme = self.label_encoder.inverse_transform([idx])[0]
                confidence = probabilities[idx]
                top_schemes.append({
                    'scheme': scheme,
                    'confidence': float(confidence)
                })
            
            return {
                'predicted_scheme': scheme_name,
                'confidence': float(probabilities[prediction]),
                'top_schemes': top_schemes
            }
            
        except Exception as e:
            return {'error': str(e)}

# Initialize DSS components
rule_engine = RuleEngine()
ml_dss = MLDSS()

@dss_bp.route('/evaluate-claim', methods=['POST'])
def evaluate_claim():
    """Evaluate claim using rule-based system"""
    try:
        data = request.get_json()
        claim_data = data.get('claim_data')
        
        if not claim_data:
            return jsonify({'error': 'No claim data provided'}), 400
        
        # Evaluate using rule engine
        matches = rule_engine.evaluate_claim(claim_data)
        
        return jsonify({
            'message': 'Claim evaluation completed',
            'matches': matches,
            'total_matches': len(matches)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dss_bp.route('/predict-schemes', methods=['POST'])
def predict_schemes():
    """Predict schemes using ML model"""
    try:
        data = request.get_json()
        claim_data = data.get('claim_data')
        
        if not claim_data:
            return jsonify({'error': 'No claim data provided'}), 400
        
        # Predict using ML model
        prediction = ml_dss.predict_schemes(claim_data)
        
        if 'error' in prediction:
            return jsonify({'error': prediction['error']}), 500
        
        return jsonify({
            'message': 'Scheme prediction completed',
            'prediction': prediction
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dss_bp.route('/train-ml-model', methods=['POST'])
def train_ml_model():
    """Train ML model for scheme matching"""
    try:
        # Get sample data (in production, this would come from database)
        claims = [
            {
                'land_area': 2.5,
                'claim_type': 'individual',
                'village': 'Sample Village',
                'district': 'Sample District',
                'state': 'Sample State'
            },
            {
                'land_area': 15.0,
                'claim_type': 'community',
                'village': 'Community Village',
                'district': 'Community District',
                'state': 'Community State'
            }
        ]
        
        scheme_matches = [
            [{'schemes': ['forest_development']}],
            [{'schemes': ['community_forest_management']}]
        ]
        
        # Train model
        result = ml_dss.train_model(claims, scheme_matches)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'message': 'ML model trained successfully',
            'results': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dss_bp.route('/rules', methods=['GET'])
def get_rules():
    """Get all decision rules"""
    try:
        return jsonify({
            'rules': rule_engine.rules,
            'total_rules': len(rule_engine.rules)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dss_bp.route('/rules', methods=['POST'])
def add_rule():
    """Add new decision rule"""
    try:
        data = request.get_json()
        new_rule = data.get('rule')
        
        if not new_rule:
            return jsonify({'error': 'No rule provided'}), 400
        
        # Add rule
        rule_engine.rules.append(new_rule)
        
        # Save rules
        rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
        with open(rules_path, 'w') as f:
            json.dump(rule_engine.rules, f, indent=2)
        
        return jsonify({
            'message': 'Rule added successfully',
            'rule': new_rule
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dss_bp.route('/comprehensive-evaluation', methods=['POST'])
def comprehensive_evaluation():
    """Comprehensive evaluation using both rule-based and ML approaches"""
    try:
        data = request.get_json()
        claim_data = data.get('claim_data')
        
        if not claim_data:
            return jsonify({'error': 'No claim data provided'}), 400
        
        # Rule-based evaluation
        rule_matches = rule_engine.evaluate_claim(claim_data)
        
        # ML-based prediction
        ml_prediction = ml_dss.predict_schemes(claim_data)
        
        # Combine results
        combined_result = {
            'rule_based_matches': rule_matches,
            'ml_prediction': ml_prediction,
            'recommendation': {
                'primary_schemes': [],
                'secondary_schemes': [],
                'confidence_score': 0.0
            }
        }
        
        # Generate recommendation
        if rule_matches and 'error' not in ml_prediction:
            # Combine rule-based and ML results
            primary_schemes = []
            secondary_schemes = []
            
            # Add top rule-based matches
            for match in rule_matches[:2]:
                primary_schemes.extend(match['schemes'])
            
            # Add ML prediction
            if ml_prediction.get('predicted_scheme'):
                primary_schemes.append(ml_prediction['predicted_scheme'])
            
            # Calculate confidence
            rule_confidence = sum(match['match_score'] for match in rule_matches[:2]) / 2 if rule_matches else 0
            ml_confidence = ml_prediction.get('confidence', 0)
            combined_confidence = (rule_confidence + ml_confidence) / 2
            
            combined_result['recommendation'] = {
                'primary_schemes': list(set(primary_schemes)),
                'secondary_schemes': secondary_schemes,
                'confidence_score': combined_confidence
            }
        
        return jsonify({
            'message': 'Comprehensive evaluation completed',
            'results': combined_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os
import numpy as np
import rasterio
from rasterio.features import shapes
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import requests
from flask import Blueprint, request, jsonify, current_app
import json
from typing import Dict, List, Tuple, Any
import cv2
from PIL import Image
import io

satellite_bp = Blueprint('satellite', __name__)

class SatelliteImageProcessor:
    """Process satellite imagery for land use classification"""
    
    def __init__(self):
        self.model = None
        self.feature_names = ['red', 'green', 'blue', 'nir', 'swir1', 'swir2', 'ndvi', 'ndwi']
        self.class_labels = {
            0: 'Water',
            1: 'Forest',
            2: 'Agricultural',
            3: 'Urban',
            4: 'Barren',
            5: 'Grassland'
        }
    
    def download_sentinel_image(self, bbox: List[float], date_range: Tuple[str, str]) -> str:
        """Download Sentinel-2 image for given bounding box and date range"""
        # This is a placeholder - in production, use Sentinel Hub API
        print(f"Downloading Sentinel-2 image for bbox: {bbox}, dates: {date_range}")
        
        # Mock implementation - return a sample image path
        sample_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'sample_satellite.tif')
        
        # Create a mock satellite image
        self._create_mock_satellite_image(sample_image_path, bbox)
        
        return sample_image_path
    
    def _create_mock_satellite_image(self, output_path: str, bbox: List[float]):
        """Create a mock satellite image for testing"""
        # Create a random multi-band image
        height, width = 1000, 1000
        bands = 6  # Red, Green, Blue, NIR, SWIR1, SWIR2
        
        # Generate random data
        data = np.random.randint(0, 255, (bands, height, width), dtype=np.uint8)
        
        # Create some realistic patterns
        # Water (blue areas)
        data[0, 400:600, 400:600] = 50  # Low red
        data[1, 400:600, 400:600] = 100  # Medium green
        data[2, 400:600, 400:600] = 200  # High blue
        
        # Forest (green areas)
        data[0, 100:300, 100:300] = 30  # Low red
        data[1, 100:300, 100:300] = 150  # High green
        data[2, 100:300, 100:300] = 50   # Low blue
        
        # Agricultural (mixed)
        data[0, 700:900, 200:400] = 100  # Medium red
        data[1, 700:900, 200:400] = 120  # Medium green
        data[2, 700:900, 200:400] = 80   # Medium blue
        
        # Save as GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=bands,
            dtype=data.dtype,
            crs='EPSG:4326',
            transform=rasterio.transform.from_bounds(
                bbox[0], bbox[1], bbox[2], bbox[3], width, height
            )
        ) as dst:
            for i in range(bands):
                dst.write(data[i], i + 1)
    
    def extract_features(self, image_path: str) -> np.ndarray:
        """Extract features from satellite image"""
        try:
            with rasterio.open(image_path) as src:
                # Read all bands
                bands = []
                for i in range(1, src.count + 1):
                    bands.append(src.read(i))
                
                # Stack bands
                image = np.stack(bands, axis=0)
                
                # Calculate indices
                red = bands[0].astype(np.float32)
                green = bands[1].astype(np.float32)
                blue = bands[2].astype(np.float32)
                nir = bands[3].astype(np.float32)
                swir1 = bands[4].astype(np.float32)
                swir2 = bands[5].astype(np.float32)
                
                # Calculate NDVI
                ndvi = np.where(
                    (nir + red) != 0,
                    (nir - red) / (nir + red),
                    0
                )
                
                # Calculate NDWI
                ndwi = np.where(
                    (green + nir) != 0,
                    (green - nir) / (green + nir),
                    0
                )
                
                # Stack all features
                features = np.stack([
                    red, green, blue, nir, swir1, swir2, ndvi, ndwi
                ], axis=0)
                
                # Reshape for ML
                features = features.reshape(features.shape[0], -1).T
                
                return features
                
        except Exception as e:
            print(f"Feature extraction error: {str(e)}")
            return np.array([])
    
    def train_model(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        """Train Random Forest classifier"""
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, labels, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Save model
            model_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'satellite_model.joblib')
            joblib.dump(self.model, model_path)
            
            return {
                'accuracy': accuracy,
                'model_path': model_path,
                'feature_importance': self.model.feature_importances_.tolist(),
                'class_labels': self.class_labels
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def predict_land_use(self, image_path: str) -> Dict[str, Any]:
        """Predict land use for satellite image"""
        try:
            if not self.model:
                # Load model if not loaded
                model_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'satellite_model.joblib')
                if os.path.exists(model_path):
                    self.model = joblib.load(model_path)
                else:
                    return {'error': 'Model not trained yet'}
            
            # Extract features
            features = self.extract_features(image_path)
            if features.size == 0:
                return {'error': 'Failed to extract features'}
            
            # Predict
            predictions = self.model.predict(features)
            probabilities = self.model.predict_proba(features)
            
            # Reshape predictions to image shape
            with rasterio.open(image_path) as src:
                pred_image = predictions.reshape(src.height, src.width)
                prob_image = probabilities.max(axis=1).reshape(src.height, src.width)
            
            # Calculate statistics
            unique_classes, counts = np.unique(predictions, return_counts=True)
            class_stats = {}
            for cls, count in zip(unique_classes, counts):
                class_stats[self.class_labels[cls]] = {
                    'pixels': int(count),
                    'percentage': float(count / len(predictions) * 100)
                }
            
            return {
                'predictions': pred_image.tolist(),
                'probabilities': prob_image.tolist(),
                'class_statistics': class_stats,
                'overall_confidence': float(np.mean(prob_image))
            }
            
        except Exception as e:
            return {'error': str(e)}

class LandUseClassifier:
    """CNN-based land use classifier (placeholder for deep learning model)"""
    
    def __init__(self):
        self.model = None
        self.input_size = (224, 224)
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for CNN"""
        try:
            # Load image
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize
            image = cv2.resize(image, self.input_size)
            
            # Normalize
            image = image.astype(np.float32) / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            print(f"Preprocessing error: {str(e)}")
            return np.array([])
    
    def train_cnn_model(self, data_path: str) -> Dict[str, Any]:
        """Train CNN model (placeholder implementation)"""
        # This is a placeholder - in production, implement actual CNN training
        return {
            'message': 'CNN training not implemented yet',
            'status': 'placeholder'
        }
    
    def predict_with_cnn(self, image_path: str) -> Dict[str, Any]:
        """Predict using CNN (placeholder implementation)"""
        # This is a placeholder - in production, implement actual CNN prediction
        return {
            'message': 'CNN prediction not implemented yet',
            'status': 'placeholder'
        }

# Initialize processors
satellite_processor = SatelliteImageProcessor()
cnn_classifier = LandUseClassifier()

@satellite_bp.route('/download-image', methods=['POST'])
def download_satellite_image():
    """Download satellite image for given area"""
    try:
        data = request.get_json()
        bbox = data.get('bbox')  # [minx, miny, maxx, maxy]
        date_range = data.get('date_range', ['2023-01-01', '2023-12-31'])
        
        if not bbox or len(bbox) != 4:
            return jsonify({'error': 'Invalid bounding box'}), 400
        
        # Download image
        image_path = satellite_processor.download_sentinel_image(bbox, tuple(date_range))
        
        return jsonify({
            'message': 'Image downloaded successfully',
            'image_path': image_path,
            'bbox': bbox,
            'date_range': date_range
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@satellite_bp.route('/extract-features', methods=['POST'])
def extract_satellite_features():
    """Extract features from satellite image"""
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'error': 'Invalid image path'}), 400
        
        # Extract features
        features = satellite_processor.extract_features(image_path)
        
        if features.size == 0:
            return jsonify({'error': 'Failed to extract features'}), 500
        
        return jsonify({
            'message': 'Features extracted successfully',
            'feature_count': features.shape[0],
            'feature_names': satellite_processor.feature_names
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@satellite_bp.route('/train-model', methods=['POST'])
def train_satellite_model():
    """Train satellite image classification model"""
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        training_data = data.get('training_data')  # Array of [features, labels]
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'error': 'Invalid image path'}), 400
        
        # Extract features
        features = satellite_processor.extract_features(image_path)
        
        if features.size == 0:
            return jsonify({'error': 'Failed to extract features'}), 500
        
        # Generate mock training labels (in production, use actual ground truth)
        labels = np.random.randint(0, 6, features.shape[0])
        
        # Train model
        result = satellite_processor.train_model(features, labels)
        
        return jsonify({
            'message': 'Model trained successfully',
            'results': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@satellite_bp.route('/predict-land-use', methods=['POST'])
def predict_land_use():
    """Predict land use for satellite image"""
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'error': 'Invalid image path'}), 400
        
        # Predict land use
        result = satellite_processor.predict_land_use(image_path)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'message': 'Land use prediction completed',
            'results': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@satellite_bp.route('/classify-with-cnn', methods=['POST'])
def classify_with_cnn():
    """Classify land use using CNN (placeholder)"""
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'error': 'Invalid image path'}), 400
        
        # CNN prediction (placeholder)
        result = cnn_classifier.predict_with_cnn(image_path)
        
        return jsonify({
            'message': 'CNN classification completed',
            'results': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

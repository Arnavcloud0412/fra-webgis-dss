import os
import cv2
import numpy as np
import pytesseract
import spacy
from PIL import Image
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import requests
from typing import Dict, List, Any

ocr_bp = Blueprint('ocr', __name__)

# Load spaCy model for NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please install: python -m spacy download en_core_web_sm")
    nlp = None

class OCRProcessor:
    """OCR processor using Tesseract"""
    
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6'
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return processed
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from image using Tesseract"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Extract text
            text = pytesseract.image_to_string(processed_img, config=self.tesseract_config)
            
            return text.strip()
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            return ""
    
    def extract_text_with_boxes(self, image_path: str) -> List[Dict]:
        """Extract text with bounding boxes"""
        try:
            processed_img = self.preprocess_image(image_path)
            
            # Get data with bounding boxes
            data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)
            
            # Filter out empty text
            boxes = []
            for i in range(len(data['text'])):
                if data['text'][i].strip():
                    boxes.append({
                        'text': data['text'][i],
                        'confidence': data['conf'][i],
                        'bbox': {
                            'x': data['left'][i],
                            'y': data['top'][i],
                            'width': data['width'][i],
                            'height': data['height'][i]
                        }
                    })
            
            return boxes
        except Exception as e:
            print(f"OCR Box Error: {str(e)}")
            return []

class NERProcessor:
    """Named Entity Recognition processor using spaCy"""
    
    def __init__(self):
        self.nlp = nlp
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        if not self.nlp:
            return {"error": "spaCy model not loaded"}
        
        doc = self.nlp(text)
        
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],  # Geopolitical entities (countries, cities, states)
            'LOC': [],  # Locations
            'DATE': [],
            'MONEY': [],
            'PERCENT': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def extract_fra_specific_entities(self, text: str) -> Dict[str, Any]:
        """Extract FRA-specific information"""
        entities = self.extract_entities(text)
        
        # Additional FRA-specific patterns
        fra_info = {
            'applicant_name': self._extract_applicant_name(text),
            'village': self._extract_village(text),
            'district': self._extract_district(text),
            'state': self._extract_state(text),
            'land_area': self._extract_land_area(text),
            'claim_type': self._extract_claim_type(text),
            'document_type': self._extract_document_type(text)
        }
        
        return {
            'general_entities': entities,
            'fra_specific': fra_info
        }
    
    def _extract_applicant_name(self, text: str) -> str:
        """Extract applicant name using patterns"""
        # Simple pattern matching - can be enhanced with ML
        lines = text.split('\n')
        for line in lines:
            if 'name' in line.lower() or 'applicant' in line.lower():
                return line.strip()
        return ""
    
    def _extract_village(self, text: str) -> str:
        """Extract village name"""
        # Pattern matching for village
        import re
        village_pattern = r'(?:village|gram|gaon)[:\s]+([A-Za-z\s]+)'
        match = re.search(village_pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_district(self, text: str) -> str:
        """Extract district name"""
        import re
        district_pattern = r'(?:district|jila)[:\s]+([A-Za-z\s]+)'
        match = re.search(district_pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_state(self, text: str) -> str:
        """Extract state name"""
        import re
        state_pattern = r'(?:state|rajya)[:\s]+([A-Za-z\s]+)'
        match = re.search(state_pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_land_area(self, text: str) -> str:
        """Extract land area"""
        import re
        area_pattern = r'(\d+(?:\.\d+)?)\s*(?:hectares?|acres?|sq\.?\s*km)'
        match = re.search(area_pattern, text, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def _extract_claim_type(self, text: str) -> str:
        """Extract claim type"""
        text_lower = text.lower()
        if 'individual' in text_lower:
            return 'individual'
        elif 'community' in text_lower:
            return 'community'
        return ""
    
    def _extract_document_type(self, text: str) -> str:
        """Extract document type"""
        text_lower = text.lower()
        if 'form' in text_lower:
            return 'form'
        elif 'certificate' in text_lower:
            return 'certificate'
        elif 'patta' in text_lower:
            return 'patta'
        return 'unknown'

# Initialize processors
ocr_processor = OCRProcessor()
ner_processor = NERProcessor()

@ocr_bp.route('/extract-text', methods=['POST'])
def extract_text():
    """Extract text from uploaded image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text
            text = ocr_processor.extract_text(filepath)
            
            return jsonify({
                'filename': filename,
                'extracted_text': text,
                'text_length': len(text)
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ocr_bp.route('/extract-with-boxes', methods=['POST'])
def extract_with_boxes():
    """Extract text with bounding boxes"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text with boxes
            boxes = ocr_processor.extract_text_with_boxes(filepath)
            
            return jsonify({
                'filename': filename,
                'text_boxes': boxes,
                'total_boxes': len(boxes)
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ocr_bp.route('/extract-entities', methods=['POST'])
def extract_entities():
    """Extract named entities from text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Extract entities
        entities = ner_processor.extract_fra_specific_entities(text)
        
        return jsonify({
            'text': text,
            'entities': entities
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ocr_bp.route('/process-document', methods=['POST'])
def process_document():
    """Complete document processing pipeline"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Step 1: Extract text
            text = ocr_processor.extract_text(filepath)
            
            # Step 2: Extract entities
            entities = ner_processor.extract_fra_specific_entities(text)
            
            # Step 3: Extract text with boxes for visualization
            boxes = ocr_processor.extract_text_with_boxes(filepath)
            
            return jsonify({
                'filename': filename,
                'extracted_text': text,
                'entities': entities,
                'text_boxes': boxes,
                'processing_status': 'completed'
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

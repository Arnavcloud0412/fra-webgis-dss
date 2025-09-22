# FRA WebGIS + Decision Support System

A comprehensive Forest Rights Act (FRA) document digitization and decision support system with WebGIS capabilities.

## 🚀 Features

- **Document Digitization**: OCR + NER for FRA document processing using Tesseract and SpaCy
- **Spatial Database**: PostgreSQL with PostGIS for structured + spatial data storage
- **Satellite Mapping**: Sentinel-2/Landsat imagery with ML land-use classification (Random Forest/CNN)
- **Interactive WebGIS**: React + Leaflet dashboard for spatial visualization
- **Decision Support**: Rule-based + ML engine for scheme matching and recommendations
- **GIS Server**: GeoServer for spatial data serving and WMS/WFS capabilities

## 📁 Project Structure

```
fra-webgis-dss/
├── backend/                 # Flask API backend
│   ├── api/               # REST endpoints (auth, claims, assets, dss, ocr, satellite)
│   ├── dss/               # Decision Support System engine
│   ├── ocr_ner/           # OCR + Named Entity Recognition pipeline
│   ├── satellite_ml/      # Satellite imagery ML classification
│   ├── app.py             # Main Flask application
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container configuration
├── frontend/              # React + Leaflet WebGIS
│   └── webgis/
│       ├── src/
│       │   ├── components/    # React components
│       │   ├── pages/         # Page components
│       │   ├── services/      # API services
│       │   └── stores/        # Zustand state management
│       ├── package.json       # Node.js dependencies
│       └── Dockerfile         # Frontend container configuration
├── gis-server/           # GeoServer configuration
│   ├── workspaces/      # GeoServer workspace configs
│   └── Dockerfile       # GeoServer container configuration
├── database/             # PostGIS database schema
│   ├── migrations/      # Database migrations
│   └── init.sql         # Initial database setup
├── docker-compose.yml    # Container orchestration
├── env.example          # Environment variables template
└── README.md           # This file
```

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **PostgreSQL + PostGIS**: Spatial database
- **JWT**: Authentication
- **Tesseract**: OCR engine
- **SpaCy**: Named Entity Recognition
- **scikit-learn**: Machine learning
- **GeoAlchemy2**: Spatial ORM

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Leaflet**: Interactive maps
- **Tailwind CSS**: Styling
- **Zustand**: State management
- **React Query**: Data fetching

### GIS & ML
- **GeoServer**: GIS server
- **Sentinel Hub API**: Satellite imagery
- **Random Forest**: Land use classification
- **OpenCV**: Image processing
- **Rasterio**: Geospatial raster I/O

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for development)
- Python 3.9+ (for development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd fra-webgis-dss
cp env.example .env
# Edit .env with your configuration
```

### 2. Start Services
```bash
# Start all services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. Initialize Database
```bash
# Run database initialization
docker-compose exec postgres psql -U fra_user -d fra_db -f /docker-entrypoint-initdb.d/init.sql
```

### 4. Access Applications
- **Frontend WebGIS**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **GeoServer**: http://localhost:8080/geoserver
- **API Documentation**: http://localhost:5000/api/docs

## 🔧 Development Setup

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export POSTGRES_HOST=localhost
export POSTGRES_DB=fra_db
export POSTGRES_USER=fra_user
export POSTGRES_PASSWORD=fra_password

# Run development server
python app.py
```

### Frontend Development
```bash
cd frontend/webgis

# Install dependencies
npm install

# Start development server
npm start
```

### Database Management
```bash
# Connect to database
docker-compose exec postgres psql -U fra_user -d fra_db

# Run migrations
docker-compose exec postgres psql -U fra_user -d fra_db -f /docker-entrypoint-initdb.d/init.sql

# Backup database
docker-compose exec postgres pg_dump -U fra_user fra_db > backup.sql
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile

### Claims Management
- `GET /api/claims` - List claims
- `POST /api/claims` - Create claim
- `GET /api/claims/{id}` - Get claim details
- `PUT /api/claims/{id}` - Update claim
- `DELETE /api/claims/{id}` - Delete claim

### Assets Management
- `GET /api/assets` - List assets
- `POST /api/assets` - Create asset
- `GET /api/assets/{id}` - Get asset details
- `PUT /api/assets/{id}` - Update asset

### OCR & Document Processing
- `POST /api/ocr/extract-text` - Extract text from image
- `POST /api/ocr/extract-entities` - Extract named entities
- `POST /api/ocr/process-document` - Complete document processing

### Satellite Analysis
- `POST /api/satellite/download-image` - Download satellite image
- `POST /api/satellite/extract-features` - Extract image features
- `POST /api/satellite/predict-land-use` - Predict land use
- `POST /api/satellite/train-model` - Train ML model

### Decision Support System
- `POST /api/dss/evaluate-claim` - Evaluate claim with rules
- `POST /api/dss/predict-schemes` - Predict schemes with ML
- `POST /api/dss/comprehensive-evaluation` - Combined evaluation
- `GET /api/dss/rules` - Get decision rules

## 🗺️ WebGIS Features

- **Interactive Maps**: Leaflet-based mapping interface
- **Layer Management**: Toggle between claims, assets, and satellite layers
- **Spatial Queries**: Find claims within distance, area calculations
- **Data Export**: Export spatial data in various formats
- **Real-time Updates**: Live data synchronization

## 🤖 Machine Learning Pipeline

### OCR + NER Pipeline
1. **Document Upload**: Accept scanned FRA documents
2. **Image Preprocessing**: Enhance image quality for OCR
3. **Text Extraction**: Use Tesseract for OCR
4. **Entity Recognition**: Extract FRA-specific entities using SpaCy
5. **Data Structuring**: Convert to structured format

### Satellite Classification
1. **Image Download**: Fetch Sentinel-2/Landsat imagery
2. **Feature Extraction**: Calculate spectral indices (NDVI, NDWI)
3. **ML Classification**: Random Forest for land use classification
4. **Confidence Scoring**: Provide classification confidence
5. **Result Visualization**: Display classification results on map

### Decision Support System
1. **Rule Engine**: Rule-based scheme matching
2. **ML Model**: Machine learning for scheme prediction
3. **Combined Evaluation**: Hybrid approach for recommendations
4. **Confidence Scoring**: Match confidence and priority

## 🔐 Security Features

- **JWT Authentication**: Secure API access
- **Role-based Access**: Admin, Officer, User roles
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Cross-origin request handling

## 📈 Monitoring & Logging

- **Health Checks**: Service health monitoring
- **Error Logging**: Comprehensive error tracking
- **Performance Metrics**: API response times
- **Database Monitoring**: Query performance tracking

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend/webgis
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📦 Deployment

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Environment Configuration
- **Development**: Local development with hot reload
- **Staging**: Pre-production testing environment
- **Production**: Production deployment with SSL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki

## 🔮 Roadmap

- [ ] Mobile app development
- [ ] Advanced ML models (CNN, Transformer)
- [ ] Real-time satellite data integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Blockchain integration for document verification

---

**Built with ❤️ for Forest Rights Act implementation and digital governance.**
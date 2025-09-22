-- FRA WebGIS DSS Database Schema
-- PostgreSQL with PostGIS extension

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create database if not exists (run this manually)
-- CREATE DATABASE fra_db;
-- \c fra_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create claims table
CREATE TABLE IF NOT EXISTS claims (
    id SERIAL PRIMARY KEY,
    claim_number VARCHAR(50) UNIQUE NOT NULL,
    applicant_name VARCHAR(100) NOT NULL,
    applicant_address TEXT,
    village VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    claim_type VARCHAR(50),
    land_area FLOAT,
    land_description TEXT,
    supporting_documents TEXT, -- JSON array of document paths
    status VARCHAR(20) DEFAULT 'pending',
    geometry GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) NOT NULL
);

-- Create assets table
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    asset_name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(50),
    area_hectares FLOAT,
    description TEXT,
    satellite_image_path VARCHAR(200),
    classification_result TEXT, -- JSON with ML classification results
    confidence_score FLOAT,
    geometry GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    claim_id INTEGER REFERENCES claims(id) NOT NULL
);

-- Create schemes table
CREATE TABLE IF NOT EXISTS schemes (
    id SERIAL PRIMARY KEY,
    scheme_name VARCHAR(100) NOT NULL,
    scheme_code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    eligibility_criteria TEXT, -- JSON with criteria
    benefits TEXT, -- JSON with benefits
    application_process TEXT,
    contact_info TEXT, -- JSON with contact details
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create spatial indexes
CREATE INDEX IF NOT EXISTS idx_claims_geometry ON claims USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_assets_geometry ON assets USING GIST (geometry);

-- Create regular indexes
CREATE INDEX IF NOT EXISTS idx_claims_user_id ON claims (user_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims (status);
CREATE INDEX IF NOT EXISTS idx_claims_village ON claims (village);
CREATE INDEX IF NOT EXISTS idx_claims_district ON claims (district);
CREATE INDEX IF NOT EXISTS idx_claims_state ON claims (state);
CREATE INDEX IF NOT EXISTS idx_assets_claim_id ON assets (claim_id);
CREATE INDEX IF NOT EXISTS idx_assets_asset_type ON assets (asset_type);

-- Insert sample data
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@fra-webgis.local', 'pbkdf2:sha256:260000$...', 'admin'),
('officer1', 'officer1@fra-webgis.local', 'pbkdf2:sha256:260000$...', 'officer'),
('user1', 'user1@fra-webgis.local', 'pbkdf2:sha256:260000$...', 'user')
ON CONFLICT (username) DO NOTHING;

-- Insert sample schemes
INSERT INTO schemes (scheme_name, scheme_code, description, eligibility_criteria, benefits, application_process, contact_info) VALUES
('Forest Development Scheme', 'forest_development', 'Support for forest development activities', 
 '{"claim_type": "individual", "land_area": {"min": 0.1, "max": 4.0}}',
 '{"financial_support": 50000, "technical_assistance": true}',
 'Submit application with land documents',
 '{"contact_person": "Forest Officer", "phone": "1234567890", "email": "forest@gov.in"}'),
 
('Community Forest Management', 'community_forest_management', 'Support for community forest management',
 '{"claim_type": "community", "land_area": {"min": 1.0, "max": 1000.0}}',
 '{"financial_support": 200000, "equipment_provided": true}',
 'Submit community resolution and land documents',
 '{"contact_person": "Community Officer", "phone": "1234567891", "email": "community@gov.in"}'),
 
('Agricultural Support Scheme', 'agricultural_support', 'Support for agricultural activities',
 '{"land_type": "agricultural", "land_area": {"min": 0.5, "max": 10.0}}',
 '{"seeds_provided": true, "irrigation_support": true}',
 'Submit land documents and crop plan',
 '{"contact_person": "Agriculture Officer", "phone": "1234567892", "email": "agriculture@gov.in"}'),
 
('Micro Finance Scheme', 'micro_finance', 'Micro finance for small landholders',
 '{"land_area": {"max": 1.0}, "income_level": "low"}',
 '{"loan_amount": 25000, "interest_rate": 4.0}',
 'Submit income certificate and land documents',
 '{"contact_person": "Finance Officer", "phone": "1234567893", "email": "finance@gov.in"}'),
 
('Tribal Development Scheme', 'tribal_development', 'Development support for tribal communities',
 '{"community_type": "tribal", "claim_type": "community"}',
 '{"educational_support": true, "healthcare_support": true}',
 'Submit tribal certificate and community documents',
 '{"contact_person": "Tribal Officer", "phone": "1234567894", "email": "tribal@gov.in"}')
ON CONFLICT (scheme_code) DO NOTHING;

-- Insert sample claims
INSERT INTO claims (claim_number, applicant_name, applicant_address, village, district, state, claim_type, land_area, land_description, status, user_id) VALUES
('FRA000001', 'Ram Singh', 'Village: Sample Village, District: Sample District', 'Sample Village', 'Sample District', 'Sample State', 'individual', 2.5, 'Forest land with mixed vegetation', 'pending', 3),
('FRA000002', 'Community Forest Committee', 'Village: Community Village, District: Community District', 'Community Village', 'Community District', 'Community State', 'community', 15.0, 'Community forest land', 'approved', 3),
('FRA000003', 'Sita Devi', 'Village: Agricultural Village, District: Agricultural District', 'Agricultural Village', 'Agricultural District', 'Agricultural State', 'individual', 1.5, 'Agricultural land', 'pending', 3)
ON CONFLICT (claim_number) DO NOTHING;

-- Insert sample assets
INSERT INTO assets (asset_name, asset_type, area_hectares, description, classification_result, confidence_score, claim_id) VALUES
('Forest Plot 1', 'forest', 2.5, 'Mixed forest with teak and bamboo', '{"predicted_class": "forest", "confidence": 0.85}', 0.85, 1),
('Community Forest', 'forest', 15.0, 'Community managed forest', '{"predicted_class": "forest", "confidence": 0.92}', 0.92, 2),
('Agricultural Field', 'agricultural', 1.5, 'Rice cultivation field', '{"predicted_class": "agricultural", "confidence": 0.78}', 0.78, 3)
ON CONFLICT DO NOTHING;

-- Create views for easier querying
CREATE OR REPLACE VIEW claim_summary AS
SELECT 
    c.id,
    c.claim_number,
    c.applicant_name,
    c.village,
    c.district,
    c.state,
    c.claim_type,
    c.land_area,
    c.status,
    c.created_at,
    u.username as created_by,
    ST_AsText(c.geometry) as geometry_wkt,
    COUNT(a.id) as asset_count
FROM claims c
LEFT JOIN users u ON c.user_id = u.id
LEFT JOIN assets a ON c.id = a.claim_id
GROUP BY c.id, c.claim_number, c.applicant_name, c.village, c.district, c.state, c.claim_type, c.land_area, c.status, c.created_at, u.username, c.geometry;

CREATE OR REPLACE VIEW asset_summary AS
SELECT 
    a.id,
    a.asset_name,
    a.asset_type,
    a.area_hectares,
    a.confidence_score,
    a.created_at,
    c.claim_number,
    c.applicant_name,
    c.village,
    c.district,
    c.state,
    ST_AsText(a.geometry) as geometry_wkt
FROM assets a
LEFT JOIN claims c ON a.claim_id = c.id;

-- Create functions for spatial operations
CREATE OR REPLACE FUNCTION get_claims_within_distance(
    input_lat FLOAT,
    input_lon FLOAT,
    distance_km FLOAT
)
RETURNS TABLE (
    claim_id INTEGER,
    claim_number VARCHAR,
    applicant_name VARCHAR,
    distance_m FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.claim_number,
        c.applicant_name,
        ST_Distance(
            ST_GeogFromText('POINT(' || input_lon || ' ' || input_lat || ')'),
            ST_Transform(c.geometry, 4326)::geography
        ) as distance_m
    FROM claims c
    WHERE ST_DWithin(
        ST_GeogFromText('POINT(' || input_lon || ' ' || input_lat || ')'),
        ST_Transform(c.geometry, 4326)::geography,
        distance_km * 1000
    );
END;
$$ LANGUAGE plpgsql;

-- Create function to calculate land area
CREATE OR REPLACE FUNCTION calculate_land_area(claim_id INTEGER)
RETURNS FLOAT AS $$
DECLARE
    area_hectares FLOAT;
BEGIN
    SELECT ST_Area(ST_Transform(geometry, 3857)) / 10000 INTO area_hectares
    FROM claims
    WHERE id = claim_id;
    
    RETURN area_hectares;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fra_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fra_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO fra_user;

-- Create update trigger for updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_claims_updated_at BEFORE UPDATE ON claims
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_schemes_updated_at BEFORE UPDATE ON schemes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert additional sample data for testing
INSERT INTO claims (claim_number, applicant_name, village, district, state, claim_type, land_area, status, user_id) VALUES
('FRA000004', 'Test User 1', 'Test Village 1', 'Test District 1', 'Test State 1', 'individual', 3.2, 'pending', 3),
('FRA000005', 'Test User 2', 'Test Village 2', 'Test District 2', 'Test State 2', 'community', 25.0, 'approved', 3),
('FRA000006', 'Test User 3', 'Test Village 3', 'Test District 3', 'Test State 3', 'individual', 0.8, 'rejected', 3)
ON CONFLICT (claim_number) DO NOTHING;

-- Create sample geometries for claims (simplified polygons)
UPDATE claims SET geometry = ST_GeomFromText('POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))', 4326) WHERE id = 1;
UPDATE claims SET geometry = ST_GeomFromText('POLYGON((77.2 28.2, 77.3 28.2, 77.3 28.3, 77.2 28.3, 77.2 28.2))', 4326) WHERE id = 2;
UPDATE claims SET geometry = ST_GeomFromText('POLYGON((77.4 28.4, 77.5 28.4, 77.5 28.5, 77.4 28.5, 77.4 28.4))', 4326) WHERE id = 3;

-- Create sample geometries for assets
UPDATE assets SET geometry = ST_GeomFromText('POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))', 4326) WHERE id = 1;
UPDATE assets SET geometry = ST_GeomFromText('POLYGON((77.2 28.2, 77.3 28.2, 77.3 28.3, 77.2 28.3, 77.2 28.2))', 4326) WHERE id = 2;
UPDATE assets SET geometry = ST_GeomFromText('POLYGON((77.4 28.4, 77.5 28.4, 77.5 28.5, 77.4 28.5, 77.4 28.4))', 4326) WHERE id = 3;

-- Create additional indexes for performance
CREATE INDEX IF NOT EXISTS idx_claims_created_at ON claims (created_at);
CREATE INDEX IF NOT EXISTS idx_assets_created_at ON assets (created_at);
CREATE INDEX IF NOT EXISTS idx_schemes_is_active ON schemes (is_active);

-- Create materialized view for dashboard statistics
CREATE MATERIALIZED VIEW dashboard_stats AS
SELECT 
    COUNT(*) as total_claims,
    COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_claims,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_claims,
    COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_claims,
    COUNT(CASE WHEN claim_type = 'individual' THEN 1 END) as individual_claims,
    COUNT(CASE WHEN claim_type = 'community' THEN 1 END) as community_claims,
    AVG(land_area) as avg_land_area,
    SUM(land_area) as total_land_area
FROM claims;

-- Create refresh function for materialized view
CREATE OR REPLACE FUNCTION refresh_dashboard_stats()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW dashboard_stats;
END;
$$ LANGUAGE plpgsql;

-- Grant execute permission on refresh function
GRANT EXECUTE ON FUNCTION refresh_dashboard_stats() TO fra_user;

-- Create a function to get scheme recommendations for a claim
CREATE OR REPLACE FUNCTION get_scheme_recommendations(claim_id INTEGER)
RETURNS TABLE (
    scheme_id INTEGER,
    scheme_name VARCHAR,
    scheme_code VARCHAR,
    match_score FLOAT,
    reason TEXT
) AS $$
DECLARE
    claim_record RECORD;
BEGIN
    -- Get claim details
    SELECT * INTO claim_record FROM claims WHERE id = claim_id;
    
    -- Return matching schemes based on simple rules
    RETURN QUERY
    SELECT 
        s.id,
        s.scheme_name,
        s.scheme_code,
        CASE 
            WHEN s.scheme_code = 'forest_development' AND claim_record.claim_type = 'individual' THEN 0.9
            WHEN s.scheme_code = 'community_forest_management' AND claim_record.claim_type = 'community' THEN 0.95
            WHEN s.scheme_code = 'agricultural_support' AND claim_record.land_area BETWEEN 0.5 AND 10.0 THEN 0.8
            WHEN s.scheme_code = 'micro_finance' AND claim_record.land_area <= 1.0 THEN 0.7
            ELSE 0.5
        END as match_score,
        CASE 
            WHEN s.scheme_code = 'forest_development' AND claim_record.claim_type = 'individual' THEN 'Individual forest rights claim'
            WHEN s.scheme_code = 'community_forest_management' AND claim_record.claim_type = 'community' THEN 'Community forest rights claim'
            WHEN s.scheme_code = 'agricultural_support' AND claim_record.land_area BETWEEN 0.5 AND 10.0 THEN 'Suitable land area for agricultural support'
            WHEN s.scheme_code = 'micro_finance' AND claim_record.land_area <= 1.0 THEN 'Small landholding eligible for micro finance'
            ELSE 'General eligibility'
        END as reason
    FROM schemes s
    WHERE s.is_active = TRUE
    ORDER BY match_score DESC;
END;
$$ LANGUAGE plpgsql;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION get_scheme_recommendations(INTEGER) TO fra_user;

-- Final message
SELECT 'FRA WebGIS DSS Database initialized successfully!' as message;

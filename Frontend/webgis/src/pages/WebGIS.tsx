import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMap } from 'react-leaflet';
import L from 'leaflet';
import { useQuery } from 'react-query';
import { MapPin, Layers, Filter, Download, Upload } from 'lucide-react';
import toast from 'react-hot-toast';
import { api } from '../services/api';

// Fix for default markers in React Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom marker icons
const createCustomIcon = (color: string) => {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  });
};

const approvedIcon = createCustomIcon('#10b981');
const pendingIcon = createCustomIcon('#f59e0b');
const rejectedIcon = createCustomIcon('#ef4444');

// Map controls component
const MapControls: React.FC<{ onLayerToggle: (layer: string) => void; activeLayers: string[] }> = ({ 
  onLayerToggle, 
  activeLayers 
}) => {
  const map = useMap();

  const layers = [
    { id: 'claims', name: 'Claims', icon: MapPin },
    { id: 'assets', name: 'Assets', icon: Layers },
    { id: 'satellite', name: 'Satellite', icon: Upload },
  ];

  return (
    <div className="absolute top-4 right-4 z-[1000] bg-white rounded-lg shadow-lg p-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3">Layers</h3>
      <div className="space-y-2">
        {layers.map((layer) => {
          const Icon = layer.icon;
          return (
            <button
              key={layer.id}
              onClick={() => onLayerToggle(layer.id)}
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm transition-colors ${
                activeLayers.includes(layer.id)
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{layer.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

// Claims data component
const ClaimsLayer: React.FC<{ claims: any[] }> = ({ claims }) => {
  return (
    <>
      {claims.map((claim) => {
        if (!claim.geometry) return null;

        try {
          // Parse WKT geometry
          const coords = claim.geometry
            .replace('POLYGON((', '')
            .replace('))', '')
            .split(',')
            .map((coord: string) => {
              const [lng, lat] = coord.trim().split(' ');
              return [parseFloat(lat), parseFloat(lng)];
            });

          const icon = claim.status === 'approved' ? approvedIcon : 
                      claim.status === 'pending' ? pendingIcon : rejectedIcon;

          return (
            <Polygon
              key={claim.id}
              positions={[coords]}
              color={claim.status === 'approved' ? '#10b981' : 
                     claim.status === 'pending' ? '#f59e0b' : '#ef4444'}
              fillColor={claim.status === 'approved' ? '#10b981' : 
                        claim.status === 'pending' ? '#f59e0b' : '#ef4444'}
              fillOpacity={0.3}
              weight={2}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold text-gray-900">{claim.claim_number}</h3>
                  <p className="text-sm text-gray-600">{claim.applicant_name}</p>
                  <p className="text-sm text-gray-600">{claim.village}, {claim.district}</p>
                  <p className="text-sm text-gray-600">Area: {claim.land_area} hectares</p>
                  <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${
                    claim.status === 'approved' ? 'bg-green-100 text-green-800' :
                    claim.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {claim.status}
                  </span>
                </div>
              </Popup>
            </Polygon>
          );
        } catch (error) {
          console.error('Error parsing geometry for claim:', claim.id, error);
          return null;
        }
      })}
    </>
  );
};

// Assets data component
const AssetsLayer: React.FC<{ assets: any[] }> = ({ assets }) => {
  return (
    <>
      {assets.map((asset) => {
        if (!asset.geometry) return null;

        try {
          // Parse WKT geometry
          const coords = asset.geometry
            .replace('POLYGON((', '')
            .replace('))', '')
            .split(',')
            .map((coord: string) => {
              const [lng, lat] = coord.trim().split(' ');
              return [parseFloat(lat), parseFloat(lng)];
            });

          const color = asset.asset_type === 'forest' ? '#059669' :
                       asset.asset_type === 'agricultural' ? '#d97706' :
                       asset.asset_type === 'urban' ? '#7c3aed' : '#6b7280';

          return (
            <Polygon
              key={asset.id}
              positions={[coords]}
              color={color}
              fillColor={color}
              fillOpacity={0.2}
              weight={1}
              dashArray="5, 5"
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold text-gray-900">{asset.asset_name}</h3>
                  <p className="text-sm text-gray-600">Type: {asset.asset_type}</p>
                  <p className="text-sm text-gray-600">Area: {asset.area_hectares} hectares</p>
                  {asset.confidence_score && (
                    <p className="text-sm text-gray-600">
                      Confidence: {(asset.confidence_score * 100).toFixed(1)}%
                    </p>
                  )}
                </div>
              </Popup>
            </Polygon>
          );
        } catch (error) {
          console.error('Error parsing geometry for asset:', asset.id, error);
          return null;
        }
      })}
    </>
  );
};

const WebGIS: React.FC = () => {
  const [activeLayers, setActiveLayers] = useState<string[]>(['claims']);
  const [mapCenter, setMapCenter] = useState<[number, number]>([28.6139, 77.2090]); // Delhi coordinates
  const [mapZoom, setMapZoom] = useState(10);

  // Fetch claims data
  const { data: claims = [], isLoading: claimsLoading } = useQuery(
    'claims',
    () => api.get('/claims').then(res => res.data.claims),
    {
      onError: (error: any) => {
        toast.error('Failed to load claims data');
        console.error('Claims fetch error:', error);
      }
    }
  );

  // Fetch assets data
  const { data: assets = [], isLoading: assetsLoading } = useQuery(
    'assets',
    () => api.get('/assets').then(res => res.data.assets),
    {
      onError: (error: any) => {
        toast.error('Failed to load assets data');
        console.error('Assets fetch error:', error);
      }
    }
  );

  const handleLayerToggle = (layerId: string) => {
    setActiveLayers(prev => 
      prev.includes(layerId) 
        ? prev.filter(id => id !== layerId)
        : [...prev, layerId]
    );
  };

  const handleExportData = () => {
    const data = {
      claims: claims,
      assets: assets,
      exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fra-webgis-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    toast.success('Data exported successfully');
  };

  if (claimsLoading || assetsLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="header p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="header-title">FRA WebGIS Dashboard</h1>
            <p className="text-sm text-gray-600 mt-1">
              Interactive mapping and spatial analysis for Forest Rights Act claims
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={handleExportData}
              className="btn-secondary flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Export Data</span>
            </button>
          </div>
        </div>
      </div>

      {/* Map Container */}
      <div className="flex-1 p-4">
        <div className="map-container">
          <MapContainer
            center={mapCenter}
            zoom={mapZoom}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {/* Map Controls */}
            <MapControls 
              onLayerToggle={handleLayerToggle} 
              activeLayers={activeLayers}
            />
            
            {/* Claims Layer */}
            {activeLayers.includes('claims') && (
              <ClaimsLayer claims={claims} />
            )}
            
            {/* Assets Layer */}
            {activeLayers.includes('assets') && (
              <AssetsLayer assets={assets} />
            )}
          </MapContainer>
        </div>
      </div>

      {/* Statistics Panel */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="stats-card">
            <div className="stats-number text-blue-600">{claims.length}</div>
            <div className="stats-label">Total Claims</div>
          </div>
          <div className="stats-card">
            <div className="stats-number text-green-600">
              {claims.filter(c => c.status === 'approved').length}
            </div>
            <div className="stats-label">Approved Claims</div>
          </div>
          <div className="stats-card">
            <div className="stats-number text-yellow-600">
              {claims.filter(c => c.status === 'pending').length}
            </div>
            <div className="stats-label">Pending Claims</div>
          </div>
          <div className="stats-card">
            <div className="stats-number text-purple-600">{assets.length}</div>
            <div className="stats-label">Total Assets</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WebGIS;

import React from 'react';
import { Satellite, Map, BarChart3 } from 'lucide-react';

const Satellite: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Satellite Imagery Analysis</h1>
        <p className="text-gray-600">ML-powered land use classification and analysis</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Map className="w-5 h-5 mr-2 text-blue-600" />
              Land Use Classification
            </h2>
            <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
              <p className="text-gray-500">Satellite imagery visualization will appear here</p>
            </div>
          </div>
        </div>

        <div>
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-green-600" />
              Classification Results
            </h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Forest</span>
                <span className="text-sm font-medium text-gray-900">45.2%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Agricultural</span>
                <span className="text-sm font-medium text-gray-900">32.1%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Urban</span>
                <span className="text-sm font-medium text-gray-900">15.3%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Water</span>
                <span className="text-sm font-medium text-gray-900">7.4%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Satellite;

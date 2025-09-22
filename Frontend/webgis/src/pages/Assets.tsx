import React from 'react';
import { Layers, Plus, MapPin } from 'lucide-react';

const Assets: React.FC = () => {
  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Assets Management</h1>
          <p className="text-gray-600">Manage spatial assets and land parcels</p>
        </div>
        <button className="btn-primary flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>New Asset</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Asset List</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <MapPin className="w-5 h-5 text-green-600" />
                  <div>
                    <p className="font-medium text-gray-900">Forest Plot 1</p>
                    <p className="text-sm text-gray-600">Forest • 2.5 hectares</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-green-600">85% Confidence</p>
                  <p className="text-xs text-gray-500">ML Classification</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Asset Types</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Forest</span>
                <span className="text-sm font-medium text-gray-900">45</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Agricultural</span>
                <span className="text-sm font-medium text-gray-900">32</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Urban</span>
                <span className="text-sm font-medium text-gray-900">18</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Water</span>
                <span className="text-sm font-medium text-gray-900">12</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Assets;

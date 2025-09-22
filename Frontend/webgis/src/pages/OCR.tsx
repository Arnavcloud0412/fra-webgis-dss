import React from 'react';
import { Camera, Upload, FileText } from 'lucide-react';

const OCR: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">OCR & Document Processing</h1>
        <p className="text-gray-600">Extract text and entities from FRA documents</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Upload className="w-5 h-5 mr-2 text-blue-600" />
            Document Upload
          </h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <Camera className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">Upload FRA documents for processing</p>
            <button className="btn-primary">Choose File</button>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <FileText className="w-5 h-5 mr-2 text-green-600" />
            Extracted Information
          </h2>
          <div className="space-y-3">
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="text-sm font-medium text-gray-900">Applicant Name</p>
              <p className="text-sm text-gray-600">Ram Singh</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="text-sm font-medium text-gray-900">Village</p>
              <p className="text-sm text-gray-600">Sample Village</p>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="text-sm font-medium text-gray-900">District</p>
              <p className="text-sm text-gray-600">Sample District</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OCR;

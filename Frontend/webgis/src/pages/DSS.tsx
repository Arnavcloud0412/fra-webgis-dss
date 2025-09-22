import React from 'react';
import { Brain, Target, Settings } from 'lucide-react';

const DSS: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Decision Support System</h1>
        <p className="text-gray-600">AI-powered scheme matching and recommendations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Brain className="w-5 h-5 mr-2 text-blue-600" />
            Scheme Recommendations
          </h2>
          <div className="space-y-4">
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="font-medium text-green-900">Forest Development Scheme</h3>
              <p className="text-sm text-green-700 mt-1">Match Score: 95%</p>
              <p className="text-xs text-green-600 mt-2">Individual forest rights claim with suitable land area</p>
            </div>
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="font-medium text-blue-900">Community Forest Management</h3>
              <p className="text-sm text-blue-700 mt-1">Match Score: 87%</p>
              <p className="text-xs text-blue-600 mt-2">Community forest rights with adequate area</p>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2 text-purple-600" />
            Rule Engine Status
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Active Rules</span>
              <span className="text-sm font-medium text-gray-900">5</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">ML Model Accuracy</span>
              <span className="text-sm font-medium text-green-600">92.3%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Last Training</span>
              <span className="text-sm font-medium text-gray-900">2 days ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DSS;

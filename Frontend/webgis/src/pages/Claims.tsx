import React from 'react';
import { FileText, Plus, Search, Filter } from 'lucide-react';

const Claims: React.FC = () => {
  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Claims Management</h1>
          <p className="text-gray-600">Manage Forest Rights Act claims</p>
        </div>
        <button className="btn-primary flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>New Claim</span>
        </button>
      </div>

      <div className="card">
        <div className="flex items-center space-x-4 mb-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search claims..."
                className="input-field pl-10"
              />
            </div>
          </div>
          <button className="btn-secondary flex items-center space-x-2">
            <Filter className="w-4 h-4" />
            <span>Filter</span>
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>Claim Number</th>
                <th>Applicant</th>
                <th>Village</th>
                <th>District</th>
                <th>Type</th>
                <th>Area (ha)</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>FRA000001</td>
                <td>Ram Singh</td>
                <td>Sample Village</td>
                <td>Sample District</td>
                <td>Individual</td>
                <td>2.5</td>
                <td>
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs">
                    Pending
                  </span>
                </td>
                <td>
                  <button className="text-blue-600 hover:text-blue-800 text-sm">View</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Claims;

import React from 'react';
import { FileText, CheckCircle, Clock, XCircle, MapPin, Users } from 'lucide-react';

const Dashboard: React.FC = () => {
  const stats = [
    { name: 'Total Claims', value: '156', icon: FileText, color: 'blue' },
    { name: 'Approved', value: '89', icon: CheckCircle, color: 'green' },
    { name: 'Pending', value: '45', icon: Clock, color: 'yellow' },
    { name: 'Rejected', value: '22', icon: XCircle, color: 'red' },
    { name: 'Assets Mapped', value: '234', icon: MapPin, color: 'purple' },
    { name: 'Active Users', value: '12', icon: Users, color: 'indigo' },
  ];

  const recentActivities = [
    { id: 1, action: 'New claim submitted', user: 'Ram Singh', time: '2 hours ago', type: 'claim' },
    { id: 2, action: 'Asset mapped', user: 'Sita Devi', time: '4 hours ago', type: 'asset' },
    { id: 3, action: 'Claim approved', user: 'Admin', time: '6 hours ago', type: 'approval' },
    { id: 4, action: 'Satellite analysis completed', user: 'System', time: '8 hours ago', type: 'analysis' },
  ];

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to FRA WebGIS Decision Support System</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="stats-card">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg bg-${stat.color}-100`}>
                  <Icon className={`w-6 h-6 text-${stat.color}-600`} />
                </div>
                <div className="ml-4">
                  <div className={`stats-number text-${stat.color}-600`}>{stat.value}</div>
                  <div className="stats-label">{stat.name}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activities */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activities</h2>
          <div className="space-y-4">
            {recentActivities.map((activity) => (
              <div key={activity.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className={`w-2 h-2 rounded-full ${
                  activity.type === 'claim' ? 'bg-blue-500' :
                  activity.type === 'asset' ? 'bg-purple-500' :
                  activity.type === 'approval' ? 'bg-green-500' :
                  'bg-yellow-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                  <p className="text-xs text-gray-600">by {activity.user} • {activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            <button className="p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors">
              <FileText className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-blue-900">New Claim</p>
            </button>
            <button className="p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors">
              <MapPin className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-green-900">Map Asset</p>
            </button>
            <button className="p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors">
              <CheckCircle className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-purple-900">Review Claims</p>
            </button>
            <button className="p-4 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition-colors">
              <Users className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
              <p className="text-sm font-medium text-yellow-900">Manage Users</p>
            </button>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="mt-6 card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">System Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-700">Database: Online</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-700">GeoServer: Online</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-700">ML Services: Online</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-700">OCR Engine: Online</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

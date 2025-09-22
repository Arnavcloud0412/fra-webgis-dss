import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  FileText, 
  Map, 
  Layers, 
  Brain, 
  Camera, 
  Satellite,
  LogOut,
  User
} from 'lucide-react';
import { useAuthStore } from '../stores/authStore';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const { user, logout } = useAuthStore();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Claims', href: '/claims', icon: FileText },
    { name: 'Assets', href: '/assets', icon: Layers },
    { name: 'WebGIS', href: '/webgis', icon: Map },
    { name: 'DSS', href: '/dss', icon: Brain },
    { name: 'OCR', href: '/ocr', icon: Camera },
    { name: 'Satellite', href: '/satellite', icon: Satellite },
  ];

  const isActive = (href: string) => {
    return location.pathname === href;
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="sidebar w-64">
        <div className="p-6">
          <h2 className="text-xl font-bold text-gray-800">FRA WebGIS DSS</h2>
          <p className="text-sm text-gray-600 mt-1">Forest Rights Act System</p>
        </div>
        
        <nav className="mt-6">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`sidebar-item ${isActive(item.href) ? 'active' : ''}`}
              >
                <Icon className="sidebar-icon" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
        
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div className="flex items-center space-x-3 mb-3">
            <User className="w-5 h-5 text-gray-600" />
            <div>
              <p className="text-sm font-medium text-gray-800">{user?.username}</p>
              <p className="text-xs text-gray-600">{user?.role}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {children}
      </div>
    </div>
  );
};

export default Layout;

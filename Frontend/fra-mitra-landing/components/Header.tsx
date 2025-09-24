import React from 'react';
import { HeartPulse } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white/80 backdrop-blur-md sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left: Logo */}
          <div className="flex-shrink-0">
            <a href="/landing" className="flex items-center space-x-2">
              {/* Placeholder for Logo */}
              <HeartPulse className="h-8 w-8 text-red-600" />
              <span className="text-xl font-bold text-gray-800">
                FRA-Mitra
              </span>
            </a>
          </div>

          {/* Right: Language Toggle */}
          <div className="flex items-center space-x-4 text-sm font-medium text-gray-600">
            <button className="hover:text-red-600 transition-colors">EN</button>
            <span className="text-gray-300">|</span>
            <button className="hover:text-red-600 transition-colors">हिंदी</button>
            <span className="text-gray-300">|</span>
            <button className="hover:text-red-600 transition-colors">मराठी</button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

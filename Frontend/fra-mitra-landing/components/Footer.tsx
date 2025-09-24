import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            {/* Placeholder for SIH Logo */}
            <div className="w-12 h-12 bg-gray-600 rounded-full flex items-center justify-center font-bold">
              SIH
            </div>
            <div>
              <p className="font-bold text-lg">Smart India Hackathon 2025</p>
            </div>
          </div>
          <div className="text-center md:text-right">
            <p className="font-semibold">Team: XCalibre</p>
            <p className="text-sm text-gray-400">Team ID: 46</p>
            <p className="mt-2 text-sm text-gray-400">
              Contact: <a href="mailto:contact@fra-mitra.gov.in" className="hover:underline">contact@fra-mitra.gov.in</a>
            </p>
          </div>
        </div>
        <div className="mt-8 pt-4 border-t border-gray-700 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} FRA-Mitra. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

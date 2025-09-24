import React from 'react';

const MapSection = () => {
  return (
    <section className="bg-white py-16 sm:py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative rounded-lg overflow-hidden shadow-2xl">
          {/* Placeholder for India Map Image */}
          <div className="bg-gray-200 h-96 flex items-center justify-center">
            <svg
              className="w-48 h-48 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1}
                d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l6.553 3.276A1 1 0 0021 19.382V8.618a1 1 0 00-.553-.894L15 5m-6 2l6-3m0 0l6-3m-6 3v10"
              />
            </svg>
          </div>
          <div className="absolute inset-0 bg-black/40 flex flex-col items-center justify-center text-center p-4">
            <h2 className="text-4xl md:text-5xl font-extrabold text-white">
              Tribal Land Holdings Across India
            </h2>
            <button className="mt-6 px-8 py-3 bg-red-600 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 transition-transform transform hover:scale-105">
              View FRA Atlas
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default MapSection;

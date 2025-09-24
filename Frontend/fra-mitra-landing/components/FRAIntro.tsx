import React from 'react';
import { Bot, Map, Satellite, Handshake } from 'lucide-react';

const pillars = [
  {
    icon: <Bot className="h-12 w-12 text-red-600" />,
    title: "AI-Powered Digitization",
    description: "Automated processing of FRA documents using advanced OCR and NER technology.",
  },
  {
    icon: <Map className="h-12 w-12 text-red-600" />,
    title: "FRA Atlas (WebGIS)",
    description: "Interactive maps for visualizing land claims, assets, and satellite data.",
  },
  {
    icon: <Satellite className="h-12 w-12 text-red-600" />,
    title: "Satellite-to-Asset Mapping",
    description: "Leveraging satellite imagery to monitor and verify land use.",
  },
  {
    icon: <Handshake className="h-12 w-12 text-red-600" />,
    title: "Intelligent Scheme Delivery",
    description: "Connecting beneficiaries with welfare schemes through a smart recommendation engine.",
  },
];

const FRAIntro = () => {
  return (
    <section className="bg-gray-50 py-16 sm:py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Introducing FRA-Mitra
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            Your Digital Partner for Land Rights
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {pillars.map((pillar) => (
            <div key={pillar.title} className="text-center p-6 bg-white rounded-lg shadow-md transition-transform transform hover:-translate-y-2">
              <div className="flex items-center justify-center h-20 w-20 mx-auto bg-red-100 rounded-full mb-4">
                {pillar.icon}
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">{pillar.title}</h3>
              <p className="text-gray-600 text-sm">{pillar.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FRAIntro;

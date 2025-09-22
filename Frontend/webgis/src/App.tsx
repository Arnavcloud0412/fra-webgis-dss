import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuthStore } from './stores/authStore';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Claims from './pages/Claims';
import Assets from './pages/Assets';
import WebGIS from './pages/WebGIS';
import DSS from './pages/DSS';
import OCR from './pages/OCR';
import Satellite from './pages/Satellite';

function App() {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/claims" element={<Claims />} />
        <Route path="/assets" element={<Assets />} />
        <Route path="/webgis" element={<WebGIS />} />
        <Route path="/dss" element={<DSS />} />
        <Route path="/ocr" element={<OCR />} />
        <Route path="/satellite" element={<Satellite />} />
      </Routes>
    </Layout>
  );
}

export default App;

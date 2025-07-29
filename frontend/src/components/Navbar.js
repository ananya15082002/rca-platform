import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, AlertTriangle } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">RCA Platform</span>
          </Link>
          
          <div className="flex items-center space-x-4">
            <Link 
              to="/dashboard" 
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Dashboard
            </Link>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <AlertTriangle className="h-4 w-4" />
              <span>Live Monitoring</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 
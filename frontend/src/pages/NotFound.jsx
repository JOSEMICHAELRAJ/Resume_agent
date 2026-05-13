import React from 'react';
import { Link } from 'react-router-dom';
import { Home, AlertCircle } from 'lucide-react';

const NotFound = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center space-y-6">
        <AlertCircle size={64} className="mx-auto text-gray-400" />
        <h1 className="text-4xl font-bold text-gray-900">404</h1>
        <p className="text-xl text-gray-600">Page Not Found</p>
        <p className="text-gray-500">The page you're looking for doesn't exist or has been moved.</p>
        <Link to="/" className="btn btn-primary inline-flex gap-2">
          <Home size={18} />
          Back to Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound;

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import UploadResumes from './pages/UploadResumes';
import CandidateMatching from './pages/CandidateMatching';
import CandidateList from './pages/CandidateList';
import JobList from './pages/JobList';
import RankingDetails from './pages/RankingDetails';
import NotFound from './pages/NotFound';
import { systemAPI } from './services/api';
import './App.css';

function App() {
  const [isConnected, setIsConnected] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    // Check backend connection
    const checkConnection = async () => {
      try {
        await systemAPI.health();
        setIsConnected(true);
      } catch (error) {
        setIsConnected(false);
        console.error('Backend connection failed:', error);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Toaster position="top-right" reverseOrder={false} />

        {/* Sidebar */}
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

        {/* Main Content */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Header */}
          <Navbar
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
            isConnected={isConnected}
          />

          {/* Page Content */}
          <main className="flex-1 overflow-y-auto">
            {!isConnected && (
              <div className="alert alert-warning shadow-lg m-4">
                <div>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="stroke-current flex-shrink-0 h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M12 9v2m0 4v2m0 4v2m0-12a9 9 0 110-18 9 9 0 010 18z"
                    />
                  </svg>
                  <span>Backend server is not reachable. Please ensure the Flask server is running.</span>
                </div>
              </div>
            )}

            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload-resumes" element={<UploadResumes />} />
              <Route path="/candidates" element={<CandidateList />} />
              <Route path="/jobs" element={<JobList />} />
              <Route path="/matching" element={<CandidateMatching />} />
              <Route path="/ranking/:rankingId" element={<RankingDetails />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;

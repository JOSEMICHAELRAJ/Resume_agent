import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Check, AlertCircle } from 'lucide-react';

const Navbar = ({ sidebarOpen, setSidebarOpen, isConnected }) => {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div className="px-6 py-4 flex items-center justify-between">
        {/* Left Section */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          <Link to="/" className="font-bold text-xl text-blue-600 hover:text-blue-700">
            🤖 ResumeAI
          </Link>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Connection Status */}
          <div className="flex items-center gap-2">
            {isConnected ? (
              <>
                <Check size={18} className="text-green-600" />
                <span className="text-sm text-green-600 font-medium">Connected</span>
              </>
            ) : (
              <>
                <AlertCircle size={18} className="text-red-600" />
                <span className="text-sm text-red-600 font-medium">Disconnected</span>
              </>
            )}
          </div>

          {/* User Menu */}
          <div className="dropdown dropdown-end">
            <button className="btn btn-ghost btn-circle avatar">
              <div className="w-10 rounded-full bg-primary flex items-center justify-center text-white font-bold">
                JD
              </div>
            </button>
            <ul
              tabIndex={0}
              className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52"
            >
              <li>
                <a href="#profile">Profile</a>
              </li>
              <li>
                <a href="#settings">Settings</a>
              </li>
              <li>
                <a href="#help">Help</a>
              </li>
              <li>
                <a href="#logout">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

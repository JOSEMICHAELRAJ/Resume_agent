import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Users,
  Briefcase,
  FileText,
  TrendingUp,
  ArrowRight,
  Calendar,
} from 'lucide-react';
import { candidateAPI, jobAPI, matchingAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalCandidates: 0,
    totalJobs: 0,
    totalMatches: 0,
    recentActivity: [],
  });
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load candidates
      const candidatesRes = await candidateAPI.list(1, 5);
      
      // Load jobs
      const jobsRes = await jobAPI.getRecruiterJobs(1, 1, 5);
      
      setStats({
        totalCandidates: candidatesRes.data.total || 0,
        totalJobs: jobsRes.data.total || 0,
        totalMatches: 0,
        recentActivity: candidatesRes.data.candidates || [],
      });
    } catch (error) {
      console.error('Error loading dashboard:', error);
      toast.showError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ icon: Icon, title, value, color }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4" style={{ borderColor: color }}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div className="p-3 rounded-lg" style={{ backgroundColor: `${color}20` }}>
          <Icon size={28} color={color} />
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="loading loading-spinner loading-lg text-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Welcome to ResumeAI</h1>
        <p className="text-gray-500 mt-2">
          AI-powered resume screening and candidate ranking system
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Users}
          title="Total Candidates"
          value={stats.totalCandidates}
          color="#3B82F6"
        />
        <StatCard
          icon={Briefcase}
          title="Job Descriptions"
          value={stats.totalJobs}
          color="#10B981"
        />
        <StatCard
          icon={FileText}
          title="Resumes Uploaded"
          value={stats.totalCandidates}
          color="#F59E0B"
        />
        <StatCard
          icon={TrendingUp}
          title="Active Matches"
          value="0"
          color="#8B5CF6"
        />
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Link
            to="/upload-resumes"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900">Upload Resumes</h3>
                <p className="text-sm text-gray-500 mt-1">Add new candidate resumes</p>
              </div>
              <ArrowRight
                size={24}
                className="text-gray-400 group-hover:text-blue-600 transition-colors"
              />
            </div>
          </Link>

          <Link
            to="/create-job"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900">Create Job</h3>
                <p className="text-sm text-gray-500 mt-1">Post a new job description</p>
              </div>
              <ArrowRight
                size={24}
                className="text-gray-400 group-hover:text-blue-600 transition-colors"
              />
            </div>
          </Link>

          <Link
            to="/candidates"
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900">View Candidates</h3>
                <p className="text-sm text-gray-500 mt-1">Browse all candidates</p>
              </div>
              <ArrowRight
                size={24}
                className="text-gray-400 group-hover:text-blue-600 transition-colors"
              />
            </div>
          </Link>
        </div>
      </div>

      {/* Recent Candidates */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Recent Candidates</h2>
          <Link to="/candidates" className="text-blue-600 hover:text-blue-700 font-medium">
            View All →
          </Link>
        </div>

        {stats.recentActivity.length > 0 ? (
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Resumes
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                    Date Added
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {stats.recentActivity.map((candidate) => (
                  <tr key={candidate.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      {candidate.full_name}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{candidate.email}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {candidate.resumes_count || 0}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      <div className="flex items-center gap-2 text-gray-500">
                        <Calendar size={16} />
                        Today
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <Users size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500">No candidates yet. Start by uploading resumes.</p>
            <Link
              to="/upload-resumes"
              className="btn btn-primary mt-4"
            >
              Upload Resumes
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

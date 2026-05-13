import React, { useState, useEffect } from 'react';
import { jobAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { Briefcase } from 'lucide-react';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      setLoading(true);
      const response = await jobAPI.getRecruiterJobs(1);
      setJobs(response.data.jobs);
    } catch (error) {
      console.error('Error loading jobs:', error);
      toast.showError('Failed to load jobs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="loading loading-spinner loading-lg text-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Jobs</h1>
        <p className="text-gray-500 mt-2">All job descriptions posted</p>
      </div>

      {jobs.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {jobs.map((job) => (
            <div key={job.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <h3 className="font-semibold text-lg text-gray-900">{job.title}</h3>
              <p className="text-gray-600 text-sm mt-1">{job.company}</p>
              <div className="mt-4 badge badge-primary">{job.candidate_count} candidates</div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <Briefcase size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">No jobs posted yet</p>
        </div>
      )}
    </div>
  );
};

export default JobList;

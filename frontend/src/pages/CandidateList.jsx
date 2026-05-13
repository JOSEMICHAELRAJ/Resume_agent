import React, { useState, useEffect } from 'react';
import { candidateAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { Search, Users } from 'lucide-react';

const CandidateList = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const toast = useToast();

  useEffect(() => {
    loadCandidates();
  }, [page]);

  const loadCandidates = async () => {
    try {
      setLoading(true);
      const response = await candidateAPI.list(page, 20);
      setCandidates(response.data.candidates);
    } catch (error) {
      console.error('Error loading candidates:', error);
      toast.showError('Failed to load candidates');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) {
      loadCandidates();
      return;
    }

    try {
      setLoading(true);
      const response = await candidateAPI.search(searchTerm);
      setCandidates(response.data.candidates);
    } catch (error) {
      console.error('Error searching candidates:', error);
      toast.showError('Search failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Candidates</h1>
        <p className="text-gray-500 mt-2">Browse and manage all candidates</p>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="max-w-md">
        <div className="join w-full">
          <input
            type="text"
            placeholder="Search by name or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input input-bordered join-item flex-1"
          />
          <button type="submit" className="btn btn-primary join-item">
            <Search size={18} />
          </button>
        </div>
      </form>

      {/* Candidates Table */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="loading loading-spinner loading-lg text-primary"></div>
        </div>
      ) : candidates.length > 0 ? (
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold">Name</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Email</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Phone</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Location</th>
                <th className="px-6 py-3 text-left text-sm font-semibold">Resumes</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {candidates.map((candidate) => (
                <tr key={candidate.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium">{candidate.full_name}</td>
                  <td className="px-6 py-4 text-sm">{candidate.email || '-'}</td>
                  <td className="px-6 py-4 text-sm">{candidate.phone || '-'}</td>
                  <td className="px-6 py-4 text-sm">{candidate.location || '-'}</td>
                  <td className="px-6 py-4 text-sm">{candidate.resumes_count || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <Users size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">No candidates found</p>
        </div>
      )}
    </div>
  );
};

export default CandidateList;

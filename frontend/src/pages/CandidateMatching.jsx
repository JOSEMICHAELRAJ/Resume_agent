import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { matchingAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { BarChart3 } from 'lucide-react';
import { getScoreColor } from '../utils/helpers';

const CandidateMatching = () => {
  const { jobId } = useParams();
  const [rankings, setRankings] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    loadRankings();
  }, [jobId]);

  const loadRankings = async () => {
    try {
      setLoading(true);
      const response = await matchingAPI.getJobRankings(jobId);
      setRankings(response.data.rankings);
    } catch (error) {
      console.error('Error loading rankings:', error);
      toast.showError('Failed to load rankings');
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
        <h1 className="text-3xl font-bold text-gray-900">Candidate Matching Results</h1>
        <p className="text-gray-500 mt-2">Top ranked candidates for this job</p>
      </div>

      {rankings.length > 0 ? (
        <div className="space-y-4">
          {rankings.map((ranking, index) => (
            <div key={ranking.ranking_id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl font-bold text-gray-400">#{index + 1}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {ranking.candidate_name}
                      </h3>
                      <p className="text-sm text-gray-500">{ranking.candidate_email}</p>
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className={`text-4xl font-bold ${getScoreColor(ranking.overall_score)}`}>
                    {ranking.overall_score.toFixed(1)}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Overall Score</p>
                </div>
              </div>

              {/* Score Breakdown */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div className="bg-blue-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Skill Match</p>
                  <p className="text-lg font-semibold text-blue-600">
                    {ranking.skill_match_score.toFixed(0)}%
                  </p>
                </div>
                <div className="bg-green-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Experience</p>
                  <p className="text-lg font-semibold text-green-600">
                    {ranking.experience_match_score.toFixed(0)}%
                  </p>
                </div>
                <div className="bg-yellow-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Education</p>
                  <p className="text-lg font-semibold text-yellow-600">
                    {ranking.education_match_score.toFixed(0)}%
                  </p>
                </div>
                <div className="bg-purple-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Semantic</p>
                  <p className="text-lg font-semibold text-purple-600">
                    {ranking.semantic_similarity_score.toFixed(0)}%
                  </p>
                </div>
              </div>

              {/* Recommendation Badge */}
              <div className="mt-4 flex items-center gap-2">
                <span className={`badge ${
                  ranking.recommendation === 'SHORTLIST'
                    ? 'badge-success'
                    : ranking.recommendation === 'PENDING'
                    ? 'badge-warning'
                    : 'badge-error'
                }`}>
                  {ranking.recommendation}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <BarChart3 size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">No matching results available</p>
        </div>
      )}
    </div>
  );
};

export default CandidateMatching;

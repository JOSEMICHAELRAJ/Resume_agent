import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { matchingAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { ArrowLeft, Download } from 'lucide-react';

const RankingDetails = () => {
  const { rankingId } = useParams();
  const navigate = useNavigate();
  const [ranking, setRanking] = useState(null);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    loadRankingDetails();
  }, [rankingId]);

  const loadRankingDetails = async () => {
    try {
      setLoading(true);
      const response = await matchingAPI.getRankingDetails(rankingId);
      setRanking(response.data);
    } catch (error) {
      console.error('Error loading ranking:', error);
      toast.showError('Failed to load ranking details');
    } finally {
      setLoading(false);
    }
  };

  const updateRecommendation = async (newRecommendation) => {
    try {
      await matchingAPI.updateRecommendation(rankingId, newRecommendation);
      setRanking((prev) => ({ ...prev, recommendation: newRecommendation }));
      toast.showSuccess(`Recommendation updated to ${newRecommendation}`);
    } catch (error) {
      console.error('Error updating recommendation:', error);
      toast.showError('Failed to update recommendation');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="loading loading-spinner loading-lg text-primary"></div>
      </div>
    );
  }

  if (!ranking) {
    return (
      <div className="p-6">
        <p className="text-gray-500">Ranking not found</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="btn btn-ghost btn-circle"
        >
          <ArrowLeft size={24} />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Ranking Details</h1>
          <p className="text-gray-500 mt-1">
            {ranking.candidate.name} for {ranking.job.title}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Candidate Info */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Candidate Information</h2>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-500">Name</p>
                <p className="text-lg font-medium">{ranking.candidate.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="text-lg">{ranking.candidate.email || 'Not provided'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Phone</p>
                <p className="text-lg">{ranking.candidate.phone || 'Not provided'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Location</p>
                <p className="text-lg">{ranking.candidate.location || 'Not provided'}</p>
              </div>
            </div>
          </div>

          {/* Scores */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Score Breakdown</h2>
            <div className="space-y-4">
              {[
                {
                  label: 'Skill Match',
                  score: ranking.scores.skill_match_score,
                  color: 'bg-blue-500',
                },
                {
                  label: 'Experience Match',
                  score: ranking.scores.experience_match_score,
                  color: 'bg-green-500',
                },
                {
                  label: 'Education Match',
                  score: ranking.scores.education_match_score,
                  color: 'bg-yellow-500',
                },
                {
                  label: 'Semantic Similarity',
                  score: ranking.scores.semantic_similarity_score,
                  color: 'bg-purple-500',
                },
              ].map((item, idx) => (
                <div key={idx}>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">{item.label}</span>
                    <span className="text-sm font-semibold text-gray-900">
                      {item.score.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${item.color}`}
                      style={{ width: `${item.score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Skills */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Skills Analysis</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="font-medium text-gray-900 mb-2">Matched Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {ranking.matched_skills?.map((skill, idx) => (
                    <span key={idx} className="badge badge-success">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="font-medium text-gray-900 mb-2">Missing Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {ranking.missing_skills?.map((skill, idx) => (
                    <span key={idx} className="badge badge-error">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Summary */}
          {ranking.summary && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">AI Summary</h2>
              <p className="text-gray-700">{ranking.summary}</p>
            </div>
          )}

          {/* Interview Questions */}
          {ranking.interview_questions && ranking.interview_questions.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Interview Questions</h2>
              <ol className="space-y-3">
                {ranking.interview_questions.map((question, idx) => (
                  <li key={idx} className="flex gap-3">
                    <span className="font-semibold text-gray-400">{idx + 1}.</span>
                    <p className="text-gray-700">{question}</p>
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Overall Score Card */}
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-md p-6 text-white">
            <p className="text-sm font-medium opacity-90">Overall Score</p>
            <p className="text-5xl font-bold mt-2">
              {ranking.scores.overall_score.toFixed(1)}
            </p>
            <p className="text-sm opacity-75 mt-2">out of 100</p>
          </div>

          {/* Recommendation */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Recommendation</h3>
            <div className="space-y-2">
              {['SHORTLIST', 'PENDING', 'REJECT'].map((rec) => (
                <button
                  key={rec}
                  onClick={() => updateRecommendation(rec)}
                  className={`w-full py-2 px-4 rounded-lg border-2 transition-colors ${
                    ranking.recommendation === rec
                      ? rec === 'SHORTLIST'
                        ? 'border-green-500 bg-green-50 text-green-700'
                        : rec === 'PENDING'
                        ? 'border-yellow-500 bg-yellow-50 text-yellow-700'
                        : 'border-red-500 bg-red-50 text-red-700'
                      : 'border-gray-200 text-gray-600 hover:border-gray-300'
                  }`}
                >
                  {rec}
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="bg-white rounded-lg shadow-md p-6 space-y-2">
            <button className="w-full btn btn-primary">
              <Download size={18} />
              Export Report
            </button>
            <button className="w-full btn btn-ghost">Send Interview Link</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RankingDetails;

import React, { useState, useEffect } from 'react';
import { candidateAPI, resumeAPI, jobAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { Search, Briefcase, FileText, Users, Sparkles } from 'lucide-react';
import { getScoreColor } from '../utils/helpers';

const CandidateMatching = () => {
  const [candidates, setCandidates] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [selectedCandidateId, setSelectedCandidateId] = useState('');
  const [selectedResumeId, setSelectedResumeId] = useState('');
  const [searchKeyword, setSearchKeyword] = useState('');
  const [resumeDetails, setResumeDetails] = useState(null);
  const [suitableJobs, setSuitableJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const toast = useToast();

  useEffect(() => {
    loadCandidates();
  }, []);

  useEffect(() => {
    if (selectedCandidateId) {
      loadCandidateResumes(selectedCandidateId);
    } else {
      setResumes([]);
      setSelectedResumeId('');
      setResumeDetails(null);
      setSuitableJobs([]);
    }
  }, [selectedCandidateId]);

  useEffect(() => {
    if (selectedResumeId) {
      loadResumeDetails(selectedResumeId);
    } else {
      setResumeDetails(null);
      setSuitableJobs([]);
    }
  }, [selectedResumeId]);

  const loadCandidates = async () => {
    try {
      setLoading(true);
      const response = await candidateAPI.list(1, 100);
      setCandidates(response.data.candidates || []);

      if ((response.data.candidates || []).length > 0) {
        setSelectedCandidateId(String(response.data.candidates[0].id));
      }
    } catch (error) {
      console.error('Error loading candidates:', error);
      toast.showError('Failed to load candidates');
    } finally {
      setLoading(false);
    }
  };

  const loadCandidateResumes = async (candidateId) => {
    try {
      const response = await resumeAPI.getCandidateResumes(candidateId);
      const candidateResumes = response.data.resumes || [];
      setResumes(candidateResumes);

      if (candidateResumes.length > 0) {
        setSelectedResumeId(String(candidateResumes[0].id));
      } else {
        setSelectedResumeId('');
        setResumeDetails(null);
      }
    } catch (error) {
      console.error('Error loading resumes:', error);
      toast.showError('Failed to load resumes for candidate');
      setResumes([]);
      setSelectedResumeId('');
      setResumeDetails(null);
    }
  };

  const loadResumeDetails = async (resumeId) => {
    try {
      const response = await resumeAPI.getResume(resumeId);
      setResumeDetails(response.data);
    } catch (error) {
      console.error('Error loading resume details:', error);
      toast.showError('Failed to load resume details');
      setResumeDetails(null);
    }
  };

  const findSuitableJobs = async () => {
    if (!selectedResumeId) {
      toast.showError('Select a resume first');
      return;
    }

    try {
      setSearching(true);
      const response = await jobAPI.getSuitableJobs({
        candidateId: selectedCandidateId || undefined,
        resumeId: selectedResumeId,
        keyword: searchKeyword.trim() || undefined,
      });

      setSuitableJobs(response.data.jobs || []);

      if ((response.data.jobs || []).length === 0) {
        toast.showError('No suitable jobs found');
      }
    } catch (error) {
      console.error('Error finding suitable jobs:', error);
      toast.showError('Failed to find suitable jobs');
    } finally {
      setSearching(false);
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
        <h1 className="text-3xl font-bold text-gray-900">Suitable Jobs</h1>
        <p className="text-gray-500 mt-2">Find jobs that fit a resume's extracted skills</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <label className="form-control">
            <span className="label-text font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Users size={16} /> Candidate
            </span>
            <select
              className="select select-bordered w-full"
              value={selectedCandidateId}
              onChange={(e) => setSelectedCandidateId(e.target.value)}
            >
              <option value="">Select candidate</option>
              {candidates.map((candidate) => (
                <option key={candidate.id} value={candidate.id}>
                  {candidate.full_name} {candidate.email ? `(${candidate.email})` : ''}
                </option>
              ))}
            </select>
          </label>

          <label className="form-control">
            <span className="label-text font-medium text-gray-700 mb-2 flex items-center gap-2">
              <FileText size={16} /> Resume
            </span>
            <select
              className="select select-bordered w-full"
              value={selectedResumeId}
              onChange={(e) => setSelectedResumeId(e.target.value)}
            >
              <option value="">Select resume</option>
              {resumes.map((resume) => (
                <option key={resume.id} value={resume.id}>
                  {resume.filename}
                </option>
              ))}
            </select>
          </label>

          <label className="form-control">
            <span className="label-text font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Search size={16} /> Job Keyword Search
            </span>
            <input
              type="text"
              className="input input-bordered w-full"
              placeholder="e.g. Python, React, Data Analyst"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
            />
          </label>
        </div>

        <button
          onClick={findSuitableJobs}
          disabled={searching || !selectedResumeId}
          className="btn btn-primary"
        >
          {searching ? (
            <>
              <span className="loading loading-spinner loading-sm"></span>
              Searching...
            </>
          ) : (
            <>
              <Sparkles size={16} /> Find Suitable Jobs
            </>
          )}
        </button>

        {resumeDetails && (
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
            <p className="font-semibold text-gray-900">Resume Skills</p>
            <div className="flex flex-wrap gap-2 mt-3">
              {Object.values(resumeDetails.skills || {})
                .flat()
                .map((skill) => (
                  <span key={skill} className="badge badge-outline badge-primary">
                    {skill}
                  </span>
                ))}
              {Object.values(resumeDetails.skills || {}).flat().length === 0 && (
                <p className="text-sm text-gray-500">No parsed skills found for this resume.</p>
              )}
            </div>
          </div>
        )}
      </div>

      {suitableJobs.length > 0 ? (
        <div className="space-y-4">
          {suitableJobs.map((job, index) => (
            <div key={job.job_id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl font-bold text-gray-400">#{index + 1}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                      <p className="text-sm text-gray-500">{job.company}</p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mt-4 line-clamp-3">{job.description}</p>
                </div>

                <div className="text-right min-w-[120px]">
                  <div className={`text-4xl font-bold ${getScoreColor(job.match_score)}`}>
                    {job.match_score.toFixed(1)}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Match Score</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <div className="bg-green-50 p-3 rounded">
                  <p className="text-xs text-gray-600 mb-2">Matched Skills</p>
                  <div className="flex flex-wrap gap-2">
                    {job.matched_skills.length > 0 ? job.matched_skills.map((skill) => (
                      <span key={skill} className="badge badge-success badge-outline">
                        {skill}
                      </span>
                    )) : (
                      <span className="text-sm text-gray-500">None</span>
                    )}
                  </div>
                </div>

                <div className="bg-red-50 p-3 rounded">
                  <p className="text-xs text-gray-600 mb-2">Missing Skills</p>
                  <div className="flex flex-wrap gap-2">
                    {job.missing_skills.length > 0 ? job.missing_skills.map((skill) => (
                      <span key={skill} className="badge badge-error badge-outline">
                        {skill}
                      </span>
                    )) : (
                      <span className="text-sm text-gray-500">None</span>
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between gap-3 flex-wrap">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Briefcase size={16} />
                  <span>{job.required_skills.length} required skill(s)</span>
                </div>
                <span className={`badge ${
                  job.recommendation === 'SUITABLE'
                    ? 'badge-success'
                    : job.recommendation === 'POTENTIAL'
                    ? 'badge-warning'
                    : 'badge-ghost'
                }`}>
                  {job.recommendation}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <Search size={48} className="mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">
            Select a resume and search to show suitable jobs based on skills.
          </p>
        </div>
      )}
    </div>
  );
};

export default CandidateMatching;

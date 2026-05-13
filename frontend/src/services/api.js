import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Resume APIs
export const resumeAPI = {
  upload: (file, candidateData = {}) => {
    const formData = new FormData();
    formData.append('file', file);
    Object.keys(candidateData).forEach((key) => {
      formData.append(key, candidateData[key]);
    });

    return api.post('/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getResume: (resumeId) => api.get(`/resume/${resumeId}`),
  getResumeText: (resumeId) => api.get(`/resume/${resumeId}/text`),
  getCandidateResumes: (candidateId) => api.get(`/resume/candidate/${candidateId}`),
  delete: (resumeId) => api.delete(`/resume/${resumeId}`),
};

// Job APIs
export const jobAPI = {
  create: (jobData) => api.post('/job/create', jobData),
  getJob: (jobId) => api.get(`/job/${jobId}`),
  getRecruiterJobs: (recruiterId, page = 1, perPage = 10) =>
    api.get(`/job/recruiter/${recruiterId}`, {
      params: { page, per_page: perPage },
    }),
  update: (jobId, jobData) => api.put(`/job/${jobId}`, jobData),
  delete: (jobId) => api.delete(`/job/${jobId}`),
};

// Candidate APIs
export const candidateAPI = {
  create: (candidateData) => api.post('/candidate/create', candidateData),
  getCandidate: (candidateId) => api.get(`/candidate/${candidateId}`),
  search: (keyword, limit = 10) =>
    api.get('/candidate/search', {
      params: { keyword, limit },
    }),
  list: (page = 1, perPage = 20) =>
    api.get('/candidate', {
      params: { page, per_page: perPage },
    }),
  update: (candidateId, candidateData) =>
    api.put(`/candidate/${candidateId}`, candidateData),
  delete: (candidateId) => api.delete(`/candidate/${candidateId}`),
  getRanking: (candidateId, jobId) =>
    api.get(`/candidate/${candidateId}/rankings/${jobId}`),
};

// Matching APIs
export const matchingAPI = {
  matchCandidates: (matchingData) => api.post('/matching/match_candidates', matchingData),
  getJobRankings: (jobId, page = 1, perPage = 20) =>
    api.get(`/matching/ranking/${jobId}`, {
      params: { page, per_page: perPage },
    }),
  getRankingDetails: (rankingId) => api.get(`/matching/ranking/${rankingId}`),
  updateRecommendation: (rankingId, recommendation) =>
    api.put(`/matching/ranking/${rankingId}`, {
      recommendation,
    }),
};

// System APIs
export const systemAPI = {
  health: () => api.get('/health'),
  info: () => api.get('/info'),
};

export default api;

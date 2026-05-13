import React, { useState } from 'react';
import { jobAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { useNavigate } from 'react-router-dom';

const CreateJob = () => {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    description: '',
    required_skills: '',
  });
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title || !formData.company || !formData.description) {
      toast.showError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    try {
      const skillsArray = formData.required_skills
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s);

      const response = await jobAPI.create({
        recruiter_id: 1, // TODO: Get from auth context
        title: formData.title,
        company: formData.company,
        description: formData.description,
        required_skills: skillsArray,
      });

      toast.showSuccess('Job description created successfully');
      navigate('/jobs');
    } catch (error) {
      console.error('Error creating job:', error);
      toast.showError('Failed to create job description');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Create Job Description</h1>
        <p className="text-gray-500 mt-2">Post a new job and our AI will match candidates</p>
      </div>

      <form onSubmit={handleSubmit} className="max-w-2xl">
        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Job Title *</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Senior Python Developer"
              className="input input-bordered w-full"
              disabled={loading}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Company *</label>
            <input
              type="text"
              name="company"
              value={formData.company}
              onChange={handleChange}
              placeholder="Tech Company Inc."
              className="input input-bordered w-full"
              disabled={loading}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe the job, responsibilities, and requirements..."
              className="textarea textarea-bordered w-full h-40"
              disabled={loading}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Required Skills
            </label>
            <textarea
              name="required_skills"
              value={formData.required_skills}
              onChange={handleChange}
              placeholder="Python, Django, MySQL, REST API (comma-separated)"
              className="textarea textarea-bordered w-full h-20"
              disabled={loading}
            />
          </div>

          <div className="flex gap-4">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading && <span className="loading loading-spinner loading-sm"></span>}
              Create Job
            </button>
            <button
              type="button"
              onClick={() => navigate('/jobs')}
              className="btn btn-ghost"
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default CreateJob;

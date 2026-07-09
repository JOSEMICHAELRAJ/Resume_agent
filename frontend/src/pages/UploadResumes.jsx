import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, CheckCircle } from 'lucide-react';
import { resumeAPI, candidateAPI } from '../services/api';
import { useToast } from '../hooks/useCustomHooks';
import { formatFileSize } from '../utils/helpers';

const UploadResumes = () => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadedResumes, setUploadedResumes] = useState([]);
  const [candidateName, setCandidateName] = useState('');
  const [candidateEmail, setCandidateEmail] = useState('');
  const toast = useToast();

  const onDrop = useCallback((acceptedFiles) => {
    const newFiles = acceptedFiles.map((file) => ({
      file,
      id: Math.random(),
      status: 'pending',
      progress: 0,
    }));
    setFiles((prev) => [...prev, ...newFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
  });

  const removeFile = (id) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const uploadResumes = async () => {
    if (files.length === 0) {
      toast.showError('Please upload at least one resume');
      return;
    }

    if (!candidateName && !candidateEmail && files.length > 1) {
      toast.showError('Please provide candidate name or email for multiple resumes');
      return;
    }

    setUploading(true);
    const uploadedList = [];

    try {
      for (const fileObj of files) {
        try {
          const response = await resumeAPI.upload(fileObj.file, {
            full_name: candidateName || 'Unknown Candidate',
            ...(candidateEmail ? { email: candidateEmail } : {}),
          });

          uploadedList.push({
            id: response.data.resume_id,
            filename: fileObj.file.name,
            candidateId: response.data.candidate_id,
            skills: response.data.parsed_data.skills,
            status: 'success',
          });

          setFiles((prev) =>
            prev.map((f) =>
              f.id === fileObj.id ? { ...f, status: 'success' } : f
            )
          );
        } catch (error) {
          console.error('Error uploading file:', error);
          setFiles((prev) =>
            prev.map((f) =>
              f.id === fileObj.id ? { ...f, status: 'error' } : f
            )
          );
          toast.showError(`Failed to upload ${fileObj.file.name}`);
        }
      }

      if (uploadedList.length > 0) {
        setUploadedResumes((prev) => [...prev, ...uploadedList]);
        toast.showSuccess(`Successfully uploaded ${uploadedList.length} resume(s)`);
        setFiles([]);
        setCandidateName('');
        setCandidateEmail('');
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Upload Resumes</h1>
        <p className="text-gray-500 mt-2">
          Upload candidate resumes (PDF or DOCX format). The system will automatically extract
          and analyze the information.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Area */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md">
            {/* Drop Zone */}
            <div
              {...getRootProps()}
              className={`
                p-12 border-2 border-dashed rounded-lg cursor-pointer
                transition-colors duration-200
                ${isDragActive
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 bg-gray-50 hover:border-gray-400'
                }
              `}
            >
              <input {...getInputProps()} />
              <div className="text-center">
                <Upload size={48} className="mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  Drag and drop your resumes here
                </h3>
                <p className="text-gray-500 mb-4">or click to browse your computer</p>
                <p className="text-sm text-gray-400">Supported formats: PDF, DOCX</p>
              </div>
            </div>

            {/* Files List */}
            {files.length > 0 && (
              <div className="mt-6 p-6 border-t border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-4">
                  Files to Upload ({files.length})
                </h3>
                <div className="space-y-3">
                  {files.map((fileObj) => (
                    <div
                      key={fileObj.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex items-center gap-3 flex-1">
                        <File size={20} className="text-gray-400" />
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">
                            {fileObj.file.name}
                          </p>
                          <p className="text-xs text-gray-500">
                            {formatFileSize(fileObj.file.size)}
                          </p>
                        </div>
                      </div>

                      {fileObj.status === 'success' && (
                        <CheckCircle size={20} className="text-green-600" />
                      )}

                      {fileObj.status === 'error' && (
                        <div className="text-red-600 text-sm">Error</div>
                      )}

                      {fileObj.status === 'pending' && (
                        <button
                          onClick={() => removeFile(fileObj.id)}
                          className="p-2 hover:bg-gray-200 rounded transition-colors"
                        >
                          <X size={20} className="text-gray-600" />
                        </button>
                      )}
                    </div>
                  ))}
                </div>

                {/* Upload Button */}
                <button
                  onClick={uploadResumes}
                  disabled={uploading}
                  className="btn btn-primary w-full mt-6"
                >
                  {uploading ? (
                    <>
                      <span className="loading loading-spinner loading-sm"></span>
                      Uploading...
                    </>
                  ) : (
                    `Upload ${files.length} Resume${files.length > 1 ? 's' : ''}`
                  )}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar - Candidate Info */}
        <div className="bg-white rounded-lg shadow-md p-6 h-fit">
          <h3 className="font-semibold text-gray-900 mb-4">Candidate Information</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name (Optional)
              </label>
              <input
                type="text"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
                placeholder="John Doe"
                className="input input-bordered w-full"
                disabled={uploading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email (Optional)
              </label>
              <input
                type="email"
                value={candidateEmail}
                onChange={(e) => setCandidateEmail(e.target.value)}
                placeholder="john@example.com"
                className="input input-bordered w-full"
                disabled={uploading}
              />
            </div>

            <div className="pt-4 border-t border-gray-200">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-700">
                  <span className="font-semibold">💡 Tip:</span> Providing candidate information
                  helps organize and categorize resumes. If not provided, generic names will be
                  used.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Uploaded Resumes */}
      {uploadedResumes.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="font-semibold text-gray-900 mb-4">
            Successfully Uploaded ({uploadedResumes.length})
          </h3>
          <div className="space-y-3">
            {uploadedResumes.map((resume) => (
              <div key={resume.id} className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                <div className="flex items-center gap-3">
                  <CheckCircle size={20} className="text-green-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{resume.filename}</p>
                    <p className="text-xs text-gray-500">
                      {Object.keys(resume.skills || {}).length} skill categories extracted
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadResumes;

import React, { useState, useEffect } from 'react';
import { jobAPI, laborerAPI } from '../services/api';

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [laborers, setLaborers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [selectedLaborers, setSelectedLaborers] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    skill_required: '',
    location: '',
    date: '',
    time: '',
    contact_number: ''
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [jobsResponse, laborersResponse] = await Promise.all([
        jobAPI.getAll(),
        laborerAPI.getAll()
      ]);
      setJobs(jobsResponse.data);
      setLaborers(laborersResponse.data);
      setError(null);
    } catch (err) {
      setError('Failed to load data');
      console.error('Jobs error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      await jobAPI.create(formData);
      
      // Reset form
      setFormData({
        title: '',
        description: '',
        skill_required: '',
        location: '',
        date: '',
        time: '',
        contact_number: ''
      });
      
      setShowForm(false);
      fetchData(); // Refresh the list
      
      alert('Job created successfully!');
    } catch (err) {
      console.error('Job creation error:', err);
      alert(err.response?.data?.detail || 'Failed to create job');
    } finally {
      setSubmitting(false);
    }
  };

  const handleAssignLaborers = async () => {
    if (selectedLaborers.length === 0) {
      alert('Please select at least one laborer');
      return;
    }

    try {
      await jobAPI.assignLaborers(selectedJob.job_id, selectedLaborers);
      setShowAssignModal(false);
      setSelectedJob(null);
      setSelectedLaborers([]);
      fetchData(); // Refresh data
      alert('Laborers assigned successfully!');
    } catch (err) {
      console.error('Assignment error:', err);
      alert(err.response?.data?.detail || 'Failed to assign laborers');
    }
  };

  const handleLaborerSelection = (phone) => {
    setSelectedLaborers(prev => 
      prev.includes(phone) 
        ? prev.filter(p => p !== phone)
        : [...prev, phone]
    );
  };

  const getAvailableLaborers = () => {
    return laborers.filter(laborer => 
      laborer.available && 
      (selectedJob?.skill_required === 'any' || laborer.skill === selectedJob?.skill_required)
    );
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
        <span className="ml-2">Loading jobs...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center fade-in">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Jobs</h2>
          <p className="mt-1 text-sm text-gray-600">
            Manage job postings and assign laborers
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          {showForm ? 'Cancel' : 'Create Job'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 fade-in">
          <div className="flex">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
              <button 
                onClick={fetchData}
                className="mt-2 text-sm text-red-600 hover:text-red-500"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Job Form */}
      {showForm && (
        <div className="card fade-in">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Create New Job</h3>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className="form-label">Job Title</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                  placeholder="e.g., House Construction - Mason Required"
                />
              </div>
              <div className="sm:col-span-2">
                <label className="form-label">Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="form-input"
                  rows={3}
                  required
                  placeholder="Describe the job requirements and details"
                />
              </div>
              <div>
                <label className="form-label">Skill Required</label>
                <select
                  name="skill_required"
                  value={formData.skill_required}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                >
                  <option value="">Select skill</option>
                  <option value="mason">Mason</option>
                  <option value="carpenter">Carpenter</option>
                  <option value="plumber">Plumber</option>
                  <option value="electrician">Electrician</option>
                  <option value="painter">Painter</option>
                  <option value="welder">Welder</option>
                  <option value="driver">Driver</option>
                  <option value="helper">Helper</option>
                  <option value="gardener">Gardener</option>
                  <option value="cleaner">Cleaner</option>
                </select>
              </div>
              <div>
                <label className="form-label">Location</label>
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                  placeholder="Job location"
                />
              </div>
              <div>
                <label className="form-label">Date</label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                />
              </div>
              <div>
                <label className="form-label">Time</label>
                <input
                  type="time"
                  name="time"
                  value={formData.time}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                />
              </div>
              <div className="sm:col-span-2">
                <label className="form-label">Contact Number</label>
                <input
                  type="tel"
                  name="contact_number"
                  value={formData.contact_number}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                  placeholder="+919876543210"
                />
              </div>
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="btn-primary flex items-center"
              >
                {submitting ? (
                  <>
                    <div className="spinner mr-2"></div>
                    Creating...
                  </>
                ) : (
                  'Create Job'
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Jobs List */}
      <div className="card fade-in">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">
            Job Postings ({jobs.length})
          </h3>
        </div>
        
        {jobs.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2V6z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No jobs posted</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new job posting.</p>
            <div className="mt-6">
              <button
                onClick={() => setShowForm(true)}
                className="btn-primary"
              >
                Create First Job
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <div key={job.job_id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="text-lg font-medium text-gray-900">{job.title}</h4>
                    <p className="mt-1 text-sm text-gray-600">{job.description}</p>
                    
                    <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
                      <div>
                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Skill</span>
                        <p className="mt-1 text-sm text-gray-900">{job.skill_required}</p>
                      </div>
                      <div>
                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Location</span>
                        <p className="mt-1 text-sm text-gray-900">{job.location}</p>
                      </div>
                      <div>
                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Date & Time</span>
                        <p className="mt-1 text-sm text-gray-900">{job.date} at {job.time}</p>
                      </div>
                      <div>
                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Contact</span>
                        <p className="mt-1 text-sm text-gray-900">{job.contact_number}</p>
                      </div>
                    </div>

                    {job.assigned_laborers.length > 0 && (
                      <div className="mt-4">
                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Assigned Laborers</span>
                        <div className="mt-1 flex flex-wrap gap-2">
                          {job.assigned_laborers.map((phone) => (
                            <span key={phone} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              {phone}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="ml-6 flex flex-col items-end space-y-2">
                    <span className={`status-${job.status}`}>
                      {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                    </span>
                    
                    {job.status === 'open' && (
                      <button
                        onClick={() => {
                          setSelectedJob(job);
                          setShowAssignModal(true);
                        }}
                        className="btn-success text-sm"
                      >
                        Assign Laborers
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Assign Laborers Modal */}
      {showAssignModal && selectedJob && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Assign Laborers to: {selectedJob.title}
              </h3>
              
              <div className="max-h-60 overflow-y-auto space-y-2">
                {getAvailableLaborers().length === 0 ? (
                  <p className="text-sm text-gray-500">No available laborers with required skill.</p>
                ) : (
                  getAvailableLaborers().map((laborer) => (
                    <label key={laborer.id} className="flex items-center space-x-3 p-2 border rounded hover:bg-gray-50">
                      <input
                        type="checkbox"
                        checked={selectedLaborers.includes(laborer.phone)}
                        onChange={() => handleLaborerSelection(laborer.phone)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{laborer.name}</p>
                        <p className="text-xs text-gray-500">{laborer.phone} • {laborer.skill}</p>
                      </div>
                    </label>
                  ))
                )}
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => {
                    setShowAssignModal(false);
                    setSelectedJob(null);
                    setSelectedLaborers([]);
                  }}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAssignLaborers}
                  className="btn-success"
                  disabled={selectedLaborers.length === 0}
                >
                  Assign ({selectedLaborers.length})
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Jobs;
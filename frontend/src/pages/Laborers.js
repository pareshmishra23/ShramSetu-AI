import React, { useState, useEffect } from 'react';
import { laborerAPI } from '../services/api';

const Laborers = () => {
  const [laborers, setLaborers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    skill: '',
    location: '',
    language: ''
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchLaborers();
  }, []);

  const fetchLaborers = async () => {
    try {
      setLoading(true);
      const response = await laborerAPI.getAll();
      setLaborers(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load laborers');
      console.error('Laborers error:', err);
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
      await laborerAPI.register(formData);
      
      // Reset form
      setFormData({
        name: '',
        phone: '',
        skill: '',
        location: '',
        language: ''
      });
      
      setShowForm(false);
      fetchLaborers(); // Refresh the list
      
      // Show success message
      alert('Laborer registered successfully!');
    } catch (err) {
      console.error('Registration error:', err);
      alert(err.response?.data?.detail || 'Failed to register laborer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (laborerId) => {
    if (window.confirm('Are you sure you want to delete this laborer?')) {
      try {
        await laborerAPI.delete(laborerId);
        fetchLaborers(); // Refresh the list
        alert('Laborer deleted successfully!');
      } catch (err) {
        console.error('Delete error:', err);
        alert('Failed to delete laborer');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
        <span className="ml-2">Loading laborers...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center fade-in">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Laborers</h2>
          <p className="mt-1 text-sm text-gray-600">
            Manage registered laborers and their information
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          {showForm ? 'Cancel' : 'Add Laborer'}
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
                onClick={fetchLaborers}
                className="mt-2 text-sm text-red-600 hover:text-red-500"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Laborer Form */}
      {showForm && (
        <div className="card fade-in">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Register New Laborer</h3>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="form-label">Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                  placeholder="Enter full name"
                />
              </div>
              <div>
                <label className="form-label">Phone</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                  placeholder="+919876543210"
                />
              </div>
              <div>
                <label className="form-label">Skill</label>
                <select
                  name="skill"
                  value={formData.skill}
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
                  placeholder="Enter location"
                />
              </div>
              <div>
                <label className="form-label">Language</label>
                <select
                  name="language"
                  value={formData.language}
                  onChange={handleInputChange}
                  className="form-input"
                  required
                >
                  <option value="">Select language</option>
                  <option value="hindi">Hindi</option>
                  <option value="english">English</option>
                  <option value="bengali">Bengali</option>
                  <option value="marathi">Marathi</option>
                  <option value="tamil">Tamil</option>
                  <option value="telugu">Telugu</option>
                  <option value="gujarati">Gujarati</option>
                  <option value="kannada">Kannada</option>
                  <option value="malayalam">Malayalam</option>
                  <option value="punjabi">Punjabi</option>
                </select>
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
                    Registering...
                  </>
                ) : (
                  'Register Laborer'
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Laborers List */}
      <div className="card fade-in">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">
            Registered Laborers ({laborers.length})
          </h3>
        </div>
        
        {laborers.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No laborers registered</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by adding a new laborer.</p>
            <div className="mt-6">
              <button
                onClick={() => setShowForm(true)}
                className="btn-primary"
              >
                Add First Laborer
              </button>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Phone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Skill
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {laborers.map((laborer) => (
                  <tr key={laborer.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                            <span className="text-sm font-medium text-gray-700">
                              {laborer.name.charAt(0).toUpperCase()}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{laborer.name}</div>
                          <div className="text-sm text-gray-500">{laborer.language}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {laborer.phone}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {laborer.skill}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {laborer.location}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={laborer.available ? 'status-available' : 'status-unavailable'}>
                        {laborer.available ? 'Available' : 'Busy'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleDelete(laborer.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Laborers;
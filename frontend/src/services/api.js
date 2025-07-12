import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Laborer API endpoints
export const laborerAPI = {
  // Get all laborers
  getAll: () => api.get('/laborers/'),
  
  // Get laborer by ID
  getById: (id) => api.get(`/laborers/${id}`),
  
  // Register new laborer
  register: (laborerData) => api.post('/laborers/register', laborerData),
  
  // Update laborer
  update: (id, updateData) => api.put(`/laborers/${id}`, updateData),
  
  // Delete laborer
  delete: (id) => api.delete(`/laborers/${id}`),
};

// Job API endpoints
export const jobAPI = {
  // Get all jobs
  getAll: () => api.get('/jobs/'),
  
  // Get job by ID
  getById: (id) => api.get(`/jobs/${id}`),
  
  // Create new job
  create: (jobData) => api.post('/jobs/create', jobData),
  
  // Update job
  update: (id, updateData) => api.put(`/jobs/${id}`, updateData),
  
  // Delete job
  delete: (id) => api.delete(`/jobs/${id}`),
  
  // Assign laborers to job
  assignLaborers: (jobId, phoneNumbers) => 
    api.patch(`/jobs/${jobId}/assign`, { phone_numbers: phoneNumbers }),
  
  // Get jobs by skill
  getBySkill: (skill) => api.get(`/jobs/skill/${skill}`),
};

// Dashboard API endpoints
export const dashboardAPI = {
  // Get summary statistics
  getSummary: async () => {
    try {
      const [laborersResponse, jobsResponse] = await Promise.all([
        laborerAPI.getAll(),
        jobAPI.getAll(),
      ]);
      
      const laborers = laborersResponse.data;
      const jobs = jobsResponse.data;
      
      return {
        totalLaborers: laborers.length,
        availableLaborers: laborers.filter(l => l.available).length,
        totalJobs: jobs.length,
        openJobs: jobs.filter(j => j.status === 'open').length,
        assignedJobs: jobs.filter(j => j.status === 'assigned').length,
        completedJobs: jobs.filter(j => j.status === 'completed').length,
      };
    } catch (error) {
      console.error('Error fetching dashboard summary:', error);
      throw error;
    }
  },
};

// Health check
export const healthCheck = () => api.get('/');

export default api;
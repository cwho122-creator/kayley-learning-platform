import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 globally
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/auth';
    }
    return Promise.reject(err);
  }
);

// ─── Auth ───────────────────────────────────────────────────────────────────
export const login = (data) => api.post('/api/auth/login', data);
export const register = (data) => api.post('/api/auth/register', data);

// ─── Lessons ────────────────────────────────────────────────────────────────
export const getSubjects = () => api.get('/api/lessons/subjects');
export const getUnits = (subjectId) => api.get(`/api/lessons/subjects/${subjectId}/units`);
export const getUnitLessons = (unitId) => api.get(`/api/lessons/units/${unitId}/lessons`);
export const getLesson = (lessonId) => api.get(`/api/lessons/${lessonId}`);
export const completeLesson = (lessonId) => api.post(`/api/lessons/${lessonId}/complete`);

// ─── Quiz ───────────────────────────────────────────────────────────────────
export const getQuizByLesson = (lessonId) => api.get(`/api/quiz/lesson/${lessonId}`);
export const submitQuiz = (quizId, data) => api.post(`/api/quiz/${quizId}/submit`, data);

// ─── Progress ───────────────────────────────────────────────────────────────
export const getProgress = () => api.get('/api/progress');
export const getBadges = () => api.get('/api/progress/badges');
export const getStreak = () => api.get('/api/progress/streak');
export const getChildren = () => api.get('/api/progress/children');
export const getChildProgress = (childId) => api.get(`/api/progress/children/${childId}`);
export const updateProfile = (data) => api.put('/api/auth/profile', data);

// ─── AI Tutor ───────────────────────────────────────────────────────────────
export const askAI = (data) => api.post('/api/ai/tutor', data);

export default api;
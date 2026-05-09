import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login, register } from '../api';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/LoadingSpinner';

export default function AuthPage() {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'student', parentEmail: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      let res;
      if (mode === 'login') {
        res = await login({ email: form.email, password: form.password });
      } else {
        const payload = {
          name: form.name,
          email: form.email,
          password: form.password,
          role: form.role,
        };
        if (form.role === 'student' && form.parentEmail) {
          payload.parent_email = form.parentEmail;
        }
        res = await register(payload);
      }
      loginUser(res.data.user, res.data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">📚</div>
        <h1 className="auth-title">Kayley's Learning Platform</h1>
        <p className="auth-subtitle">Learning made fun, one step at a time! 🌟</p>

        <div className="auth-tabs">
          <button className={`auth-tab ${mode === 'login' ? 'active' : ''}`} onClick={() => setMode('login')}>Login</button>
          <button className={`auth-tab ${mode === 'register' ? 'active' : ''}`} onClick={() => setMode('register')}>Sign Up</button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'register' && (
            <div className="form-group">
              <label>Your Name</label>
              <input type="text" value={form.name} onChange={(e) => set('name', e.target.value)} placeholder="e.g. Kayley" required />
            </div>
          )}
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={form.email} onChange={(e) => set('email', e.target.value)} placeholder="you@example.com" required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" value={form.password} onChange={(e) => set('password', e.target.value)} placeholder="••••••••" required />
          </div>
          {mode === 'register' && (
            <>
              <div className="form-group">
                <label>I am a...</label>
                <select value={form.role} onChange={(e) => set('role', e.target.value)}>
                  <option value="student">🧒 Student</option>
                  <option value="parent">👨‍👩‍👧 Parent</option>
                </select>
              </div>
              {form.role === 'student' && (
                <div className="form-group">
                  <label>Parent's Email <span className="optional">(optional)</span></label>
                  <input type="email" value={form.parentEmail} onChange={(e) => set('parentEmail', e.target.value)} placeholder="parent@example.com" />
                </div>
              )}
            </>
          )}

          {error && <div className="auth-error">{error}</div>}

          {loading ? (
            <LoadingSpinner message="Logging you in..." />
          ) : (
            <button type="submit" className="auth-btn">
              {mode === 'login' ? 'Login' : 'Create Account'} 🚀
            </button>
          )}
        </form>
      </div>

      <style>{`
        .auth-page {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
          background: linear-gradient(135deg, #EEF2FF 0%, #F3F4F6 100%);
        }
        .auth-card {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 2.5rem 2rem;
          width: 100%;
          max-width: 420px;
          box-shadow: var(--shadow-lg);
        }
        .auth-logo { font-size: 3rem; text-align: center; margin-bottom: 0.5rem; }
        .auth-title { text-align: center; font-size: 1.5rem; font-weight: 800; color: var(--primary); margin-bottom: 0.25rem; }
        .auth-subtitle { text-align: center; color: var(--text-light); margin-bottom: 1.75rem; font-size: 0.9rem; }
        .auth-tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
        .auth-tab {
          flex: 1; padding: 0.6rem;
          border: 2px solid var(--border);
          border-radius: var(--radius);
          background: none;
          font-weight: 700;
          font-size: 0.9rem;
          color: var(--text-light);
          cursor: pointer;
          transition: all 0.2s;
        }
        .auth-tab.active { border-color: var(--primary); background: #EEF2FF; color: var(--primary); }
        .auth-form { display: flex; flex-direction: column; gap: 1rem; }
        .form-group { display: flex; flex-direction: column; gap: 0.35rem; }
        .form-group label { font-weight: 600; font-size: 0.85rem; color: var(--text); }
        .form-group .optional { font-weight: 400; color: var(--text-light); font-size: 0.78rem; }
        .form-group input, .form-group select {
          padding: 0.7rem 0.875rem;
          border: 2px solid var(--border);
          border-radius: var(--radius);
          font-size: 0.95rem;
          transition: border-color 0.2s;
          background: var(--card);
        }
        .form-group input:focus, .form-group select:focus {
          outline: none;
          border-color: var(--primary);
        }
        .auth-error {
          background: #FEE2E2; color: #991B1B;
          padding: 0.75rem; border-radius: var(--radius);
          font-size: 0.85rem; font-weight: 600;
        }
        .auth-btn {
          background: var(--primary);
          color: white;
          border: none;
          border-radius: var(--radius);
          padding: 0.875rem;
          font-size: 1rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.2s;
          margin-top: 0.25rem;
        }
        .auth-btn:hover { background: var(--primary-dark); transform: translateY(-1px); }
      `}</style>
    </div>
  );
}
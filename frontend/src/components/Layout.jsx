import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };

  const isParent = user?.role === 'parent';
  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-logo">
          <span className="logo-icon">📚</span>
          <span className="logo-text">Kayley's Platform</span>
        </div>
        <div className="nav-links">
          <Link to="/dashboard" className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}>
            🏠 Dashboard
          </Link>
          <Link to="/lessons" className={`nav-link ${isActive('/lessons') ? 'active' : ''}`}>
            📖 Lessons
          </Link>
          <Link to="/ai-tutor" className={`nav-link ${isActive('/ai-tutor') ? 'active' : ''}`}>
            🤖 AI Tutor
          </Link>
          {isParent && (
            <Link to="/parent-dashboard" className={`nav-link ${isActive('/parent-dashboard') ? 'active' : ''}`}>
              👨👩 Parent Dashboard
            </Link>
          )}
          <button onClick={handleLogout} className="nav-link nav-logout">
            🚪 Logout
          </button>
        </div>
      </nav>
      <main className="layout-main">
        {/* Content injected by react-router */}
      </main>
      <style>{`
        .layout { min-height: 100vh; display: flex; flex-direction: column; }
        .navbar {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 0.75rem 1.5rem;
          display: flex;
          align-items: center;
          justify-content: space-between;
          box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        .nav-logo { display: flex; align-items: center; gap: 0.5rem; }
        .logo-icon { font-size: 1.5rem; }
        .logo-text { color: white; font-size: 1.2rem; font-weight: 700; }
        .nav-links { display: flex; gap: 0.25rem; align-items: center; }
        .nav-link {
          color: rgba(255,255,255,0.85);
          text-decoration: none;
          padding: 0.5rem 0.75rem;
          border-radius: 8px;
          font-size: 0.9rem;
          font-weight: 500;
          transition: all 0.2s;
          background: none;
          border: none;
          cursor: pointer;
        }
        .nav-link:hover, .nav-link.active {
          background: rgba(255,255,255,0.2);
          color: white;
        }
        .nav-logout { color: rgba(255,255,255,0.6); }
        .nav-logout:hover { color: white; background: rgba(255,100,100,0.2); }
        .layout-main { flex: 1; padding: 1.5rem; max-width: 1200px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        @media (max-width: 768px) {
          .navbar { flex-direction: column; gap: 0.5rem; padding: 0.75rem; }
          .nav-links { flex-wrap: wrap; justify-content: center; }
          .layout-main { padding: 1rem; }
        }
      `}</style>
    </div>
  );
}

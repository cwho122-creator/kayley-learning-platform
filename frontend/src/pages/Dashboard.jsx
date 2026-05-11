import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';
import './Dashboard.css';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        // Get user info
        const userResponse = await client.get('/auth/me');
        setUser(userResponse.data);

        // Get dashboard data
        const dashResponse = await client.get('/progress/dashboard');
        setDashboard(dashResponse.data);

        // Get subjects and lessons
        const subjectsResponse = await client.get('/lessons/subjects');
        setSubjects(subjectsResponse.data);
      } catch (err) {
        console.error('Error loading data:', err);
        if (err.response?.status === 401) {
          localStorage.removeItem('token');
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleStartLesson = async (lessonId) => {
    // TODO: Navigate to lesson player
    alert(`Starting lesson ${lessonId}`);
  };

  if (loading) {
    return <div style={{ textAlign: 'center', paddingTop: '50px' }}>Loading...</div>;
  }

  return (
    <div className="dashboard-container">
      <div className="navbar">
        <h1>🎓 {user?.full_name}'s Dashboard</h1>
        <div className="nav-actions">
          <span>👋 Welcome back!</span>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <h3>💎 Total Points</h3>
            <p className="stat-value">{dashboard?.total_points || 0}</p>
          </div>
          <div className="stat-card">
            <h3>🔥 Current Streak</h3>
            <p className="stat-value">{dashboard?.current_streak || 0}</p>
          </div>
          <div className="stat-card">
            <h3>📚 Lessons Completed</h3>
            <p className="stat-value">{dashboard?.lessons_completed || 0}</p>
          </div>
          <div className="stat-card">
            <h3>✅ Quizzes Passed</h3>
            <p className="stat-value">{dashboard?.quizzes_passed || 0}</p>
          </div>
        </div>

        {/* Badges */}
        {dashboard?.badges && dashboard.badges.length > 0 && (
          <div className="badges-section">
            <h2>🏆 Your Badges</h2>
            <div className="badges-grid">
              {dashboard.badges.map((badge) => (
                <div key={badge.id} className="badge">
                  <div className="badge-icon">{badge.icon_emoji}</div>
                  <p className="badge-name">{badge.badge_name}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Lessons */}
        <div className="lessons-section">
          <h2>📖 Available Lessons</h2>
          {subjects.map((subject) => (
            <div key={subject.id} className="subject">
              <h3 style={{ color: subject.color }}>{subject.name}</h3>
              {subject.units.map((unit) => (
                <div key={unit.id} className="unit">
                  <h4>{unit.title}</h4>
                  <div className="lessons-list">
                    {unit.lessons.map((lesson) => (
                      <div key={lesson.id} className="lesson-card">
                        <h5>{lesson.title}</h5>
                        <p>{lesson.duration_minutes} min</p>
                        <button
                          className="btn-start"
                          onClick={() => handleStartLesson(lesson.id)}
                        >
                          Start Lesson
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

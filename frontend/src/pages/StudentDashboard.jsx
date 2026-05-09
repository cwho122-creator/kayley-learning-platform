import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProgress, getBadges, getStreak } from '../api';
import { useAuth } from '../context/AuthContext';
import BadgeCard from '../components/BadgeCard';
import ProgressBar from '../components/ProgressBar';
import LoadingSpinner from '../components/LoadingSpinner';

export default function StudentDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [progress, setProgress] = useState(null);
  const [badges, setBadges] = useState([]);
  const [streak, setStreak] = useState(null);
  const [loading, setLoading] = useState(true);
  const [movementDismissed, setMovementDismissed] = useState(false);
  const [showMovement, setShowMovement] = useState(false);

  useEffect(() => {
    loadData();
    const t = setTimeout(() => setShowMovement(true), 30000);
    return () => clearTimeout(t);
  }, []);

  const loadData = async () => {
    try {
      const [progRes, badgeRes, streakRes] = await Promise.all([
        getProgress().catch(() => ({ data: null })),
        getBadges().catch(() => ({ data: [] })),
        getStreak().catch(() => ({ data: { current: 0 } })),
      ]);
      setProgress(progRes.data);
      setBadges(badgeRes.data || []);
      setStreak(streakRes.data);
    } catch {
      setProgress(null);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading your dashboard..." />;

  const displayName = user?.name === 'Kayley' ? 'Kayley' : user?.name || 'there';
  const totalPoints = progress?.total_points ?? 0;
  const currentStreak = streak?.current ?? 0;
  const lessonsCompleted = progress?.lessons_completed ?? 0;
  const subjectProgress = progress?.subject_progress ?? [];

  return (
    <div className="sdash">
      {showMovement && !movementDismissed && (
        <div className="sdash-movement-banner" onClick={() => setMovementDismissed(true)}>
          🧘‍♀️ Time for a movement break! <button onClick={(e) => { e.stopPropagation(); setMovementDismissed(true); }}>Dismiss</button>
        </div>
      )}

      <div className="sdash-welcome">
        <h1>Hi {displayName}! 👋</h1>
        <p>Ready to learn something awesome today? Let's go! 🚀</p>
      </div>

      <div className="sdash-stats">
        <div className="sdash-stat">
          <div className="stat-icon">🔥</div>
          <div>
            <div className="stat-value">{currentStreak}</div>
            <div className="stat-label">Day Streak</div>
          </div>
        </div>
        <div className="sdash-stat">
          <div className="stat-icon">⭐</div>
          <div>
            <div className="stat-value">{totalPoints}</div>
            <div className="stat-label">Total Points</div>
          </div>
        </div>
        <div className="sdash-stat">
          <div className="stat-icon">📖</div>
          <div>
            <div className="stat-value">{lessonsCompleted}</div>
            <div className="stat-label">Lessons Done</div>
          </div>
        </div>
      </div>

      <div className="sdash-actions">
        <button className="sdash-action-btn primary" onClick={() => navigate('/lessons')}>
          📖 Start Lesson
        </button>
        <button className="sdash-action-btn secondary" onClick={() => navigate('/lessons')}>
          📝 Take Quiz
        </button>
        <button className="sdash-action-btn accent" onClick={() => navigate('/ai-tutor')}>
          🤖 Ask AI Tutor
        </button>
      </div>

      {subjectProgress.length > 0 && (
        <div className="sdash-section">
          <h2>📊 Your Progress</h2>
          <div className="sdash-subjects">
            {subjectProgress.map((s) => (
              <div key={s.subject_id} className="sdash-subject-card">
                <div className="sdash-subject-header">
                  <span className="subj-emoji">{s.subject === 'Math' ? '🔢' : '🔬'}</span>
                  <span className="subj-name">{s.subject}</span>
                </div>
                <ProgressBar percent={s.percent} subject={s.subject?.toLowerCase()} />
                <p className="subj-lessons">{s.completed}/{s.total} lessons</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {badges.length > 0 && (
        <div className="sdash-section">
          <h2>🏆 Your Badges</h2>
          <div className="sdash-badges">
            {badges.map((b, i) => (
              <BadgeCard key={i} emoji={b.emoji || '🏅'} name={b.name} description={b.description} isNew={b.is_new} />
            ))}
          </div>
        </div>
      )}

      <style>{`
        .sdash { max-width: 800px; margin: 0 auto; }
        .sdash-movement-banner {
          background: #FEF9C3;
          border: 2px solid #FDE047;
          border-radius: var(--radius);
          padding: 0.75rem 1rem;
          margin-bottom: 1.25rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-weight: 600;
          cursor: pointer;
        }
        .sdash-movement-banner button {
          background: none; border: none; cursor: pointer; font-weight: 700; color: var(--primary);
        }
        .sdash-welcome h1 { font-size: 1.75rem; font-weight: 800; color: var(--primary); margin-bottom: 0.25rem; }
        .sdash-welcome p { color: var(--text-light); font-size: 1rem; }
        .sdash-stats {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1rem;
          margin: 1.5rem 0;
        }
        .sdash-stat {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 1.25rem;
          box-shadow: var(--shadow);
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        .stat-icon { font-size: 2rem; }
        .stat-value { font-size: 1.5rem; font-weight: 800; line-height: 1.2; }
        .stat-label { font-size: 0.78rem; color: var(--text-light); font-weight: 600; }
        .sdash-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 2rem; }
        .sdash-action-btn {
          flex: 1; min-width: 140px;
          padding: 0.875rem;
          border: none;
          border-radius: var(--radius);
          font-weight: 700;
          font-size: 0.95rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .sdash-action-btn.primary { background: var(--primary); color: white; }
        .sdash-action-btn.secondary { background: var(--card); color: var(--text); box-shadow: var(--shadow); border: 2px solid var(--border); }
        .sdash-action-btn.accent { background: #F5F3FF; color: var(--primary); }
        .sdash-action-btn:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
        .sdash-section { margin-bottom: 2rem; }
        .sdash-section h2 { font-size: 1.15rem; font-weight: 800; margin-bottom: 0.875rem; }
        .sdash-subjects { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1rem; }
        .sdash-subject-card {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 1rem;
          box-shadow: var(--shadow);
        }
        .sdash-subject-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem; }
        .subj-emoji { font-size: 1.25rem; }
        .subj-name { font-weight: 700; font-size: 0.95rem; }
        .subj-lessons { font-size: 0.75rem; color: var(--text-light); margin-top: 0.4rem; text-align: right; }
        .sdash-badges { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 0.75rem; }
        @media (max-width: 600px) {
          .sdash-stats { grid-template-columns: 1fr; }
          .stat-value { font-size: 1.25rem; }
        }
      `}</style>
    </div>
  );
}
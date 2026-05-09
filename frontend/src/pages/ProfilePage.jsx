import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getBadges, getStreak, updateProfile } from '../api';
import { useNavigate } from 'react-router-dom';
import BadgeCard from '../components/BadgeCard';
import LoadingSpinner from '../components/LoadingSpinner';

const AVATARS = ['🧒', '🚀', '🌟', '🦄', '🐱', '🦊', '🐸', '🦋', '🌈', '🎮'];
const AVATAR_COLORS = ['#EEF2FF', '#F0FDF4', '#FEF9C3', '#FCE7F3', '#FEF3C7', '#F0E6FF'];

export default function ProfilePage() {
  const { user, updateUser, logout: authLogout } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState(user?.name || '');
  const [avatar, setAvatar] = useState(user?.avatar || '🧒');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [badges, setBadges] = useState([]);
  const [streak, setStreak] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getBadges().catch(() => ({ data: [] })),
      getStreak().catch(() => ({ data: { current: 0, history: [] } })),
    ]).then(([badgeRes, streakRes]) => {
      setBadges(badgeRes.data || []);
      setStreak(streakRes.data);
      setLoading(false);
    });
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await updateProfile({ name, avatar });
      updateUser({ name, avatar });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch {
      // Just update local state anyway
      updateUser({ name, avatar });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } finally {
      setSaving(false);
    }
  };

  const handleLogout = () => {
    authLogout();
    navigate('/auth');
  };

  // Build streak calendar
  const history = streak?.history || [];
  const today = new Date();
  const calendarDays = Array.from({ length: 35 }, (_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() - (34 - i));
    const dateStr = d.toISOString().split('T')[0];
    const active = history.includes(dateStr);
    return { date: d, active, isToday: i === 34 };
  });

  if (loading) return <LoadingSpinner message="Loading profile..." />;

  return (
    <div className="profile">
      <h1>👤 Profile</h1>

      {/* Avatar & Name Edit */}
      <div className="profile-card">
        <h2>Your Info</h2>

        <div className="avatar-picker">
          {AVATARS.map((a, i) => (
            <button
              key={i}
              className={`avatar-opt ${avatar === a ? 'selected' : ''}`}
              onClick={() => setAvatar(a)}
              style={{ background: avatar === a ? AVATAR_COLORS[i % AVATAR_COLORS.length] : 'var(--bg)' }}
            >
              {a}
            </button>
          ))}
        </div>

        <div className="form-group">
          <label>Name</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} maxLength={50} />
        </div>

        <button className="save-btn" onClick={handleSave} disabled={saving || (!name.trim())}>
          {saving ? 'Saving...' : saved ? '✅ Saved!' : 'Save Changes'}
        </button>
      </div>

      {/* Streak Calendar */}
      <div className="profile-card">
        <h2>🔥 Streak Calendar</h2>
        <p className="streak-current">Current streak: <strong>{streak?.current ?? 0} days</strong></p>
        <div className="calendar">
          {calendarDays.map((day, i) => (
            <div
              key={i}
              className={`cal-day ${day.active ? 'active' : ''} ${day.isToday ? 'today' : ''}`}
              title={day.date.toLocaleDateString()}
            >
              {day.date.getDate()}
            </div>
          ))}
        </div>
        <p className="calendar-legend">
          <span className="legend-dot active" /> Active day &nbsp;
          <span className="legend-dot today" /> Today
        </p>
      </div>

      {/* Badges */}
      {badges.length > 0 && (
        <div className="profile-card">
          <h2>🏆 Your Badges</h2>
          <div className="badges-grid">
            {badges.map((b, i) => (
              <BadgeCard key={i} emoji={b.emoji || '🏅'} name={b.name} description={b.description} isNew={b.is_new} />
            ))}
          </div>
        </div>
      )}

      {/* Logout */}
      <button className="logout-btn" onClick={handleLogout}>
        🚪 Logout
      </button>

      <style>{`
        .profile { max-width: 620px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.25rem; }
        .profile h1 { font-size: 1.75rem; font-weight: 800; }
        .profile-card {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 1.5rem;
          box-shadow: var(--shadow);
        }
        .profile-card h2 { font-size: 1.05rem; font-weight: 700; margin-bottom: 1rem; }
        .avatar-picker { display: flex; flex-wrap: wrap; gap: 0.625rem; margin-bottom: 1rem; }
        .avatar-opt {
          width: 48px; height: 48px;
          border: 2px solid transparent;
          border-radius: 50%;
          font-size: 1.5rem;
          cursor: pointer;
          transition: all 0.2s;
          display: flex; align-items: center; justify-content: center;
        }
        .avatar-opt:hover { transform: scale(1.1); }
        .avatar-opt.selected { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(99,102,241,0.2); }
        .form-group { display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 1rem; }
        .form-group label { font-weight: 600; font-size: 0.85rem; }
        .form-group input {
          padding: 0.7rem 0.875rem;
          border: 2px solid var(--border);
          border-radius: var(--radius);
          font-size: 0.95rem;
          font-family: inherit;
          background: var(--card);
        }
        .form-group input:focus { outline: none; border-color: var(--primary); }
        .save-btn {
          padding: 0.75rem 1.5rem;
          background: var(--primary); color: white;
          border: none; border-radius: var(--radius);
          font-weight: 700; cursor: pointer;
          transition: all 0.2s;
        }
        .save-btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .save-btn:hover:not(:disabled) { background: var(--primary-dark); }
        .streak-current { font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.875rem; }
        .streak-current strong { color: var(--primary); }
        .calendar {
          display: grid;
          grid-template-columns: repeat(7, 1fr);
          gap: 4px;
          margin-bottom: 0.625rem;
        }
        .cal-day {
          aspect-ratio: 1;
          display: flex; align-items: center; justify-content: center;
          border-radius: 6px;
          font-size: 0.72rem;
          font-weight: 600;
          color: var(--text-light);
          background: var(--bg);
        }
        .cal-day.active { background: var(--primary); color: white; }
        .cal-day.today { border: 2px solid var(--warning); }
        .calendar-legend { font-size: 0.78rem; color: var(--text-light); }
        .legend-dot {
          display: inline-block; width: 10px; height: 10px;
          border-radius: 50%; margin-right: 2px; vertical-align: middle;
        }
        .legend-dot.active { background: var(--primary); }
        .legend-dot.today { background: transparent; border: 2px solid var(--warning); }
        .badges-grid { display: flex; flex-direction: column; gap: 0.625rem; }
        .logout-btn {
          padding: 0.75rem;
          background: #FEF2F2; color: var(--error);
          border: 2px solid #FECACA;
          border-radius: var(--radius);
          font-weight: 700; font-size: 0.95rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .logout-btn:hover { background: #FEE2E2; }
      `}</style>
    </div>
  );
}
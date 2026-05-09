import React, { useEffect, useState } from 'react';
import { getChildren, getChildProgress } from '../api';
import BadgeCard from '../components/BadgeCard';
import LoadingSpinner from '../components/LoadingSpinner';

function SimpleBarChart({ data }) {
  if (!data || data.length === 0) return <p className="no-data">No data yet 📊</p>;
  const max = Math.max(...data.map((d) => d.count), 1);
  return (
    <div className="bar-chart">
      {data.map((d, i) => (
        <div key={i} className="bar-row">
          <span className="bar-label">{d.label}</span>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${(d.count / max) * 100}%` }} />
          </div>
          <span className="bar-count">{d.count}</span>
        </div>
      ))}
    </div>
  );
}

function ChildCard({ child }) {
  const [expanded, setExpanded] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [progressData, setProgressData] = useState(null);

  useEffect(() => {
    if (expanded) {
      getChildProgress(child.id)
        .then((r) => setProgressData(r.data))
        .catch(() => setProgressData(null));
    }
  }, [expanded, child.id]);

  const weekly = progressData?.weekly_lessons || [];
  const quizAvg = progressData?.quiz_average || 0;

  return (
    <div className="child-card">
      <button className="child-header" onClick={() => setExpanded(!expanded)}>
        <div className="child-info">
          <span className="child-avatar">🧒</span>
          <div>
            <p className="child-name">{child.name || child.email}</p>
            <p className="child-email">{child.email}</p>
          </div>
        </div>
        <div className="child-stats">
          <span className="child-stat">⭐ {child.total_points ?? 0} pts</span>
          <span className="child-stat">🔥 {child.streak ?? 0} day streak</span>
          <span className="child-toggle">{expanded ? '▲' : '▼'}</span>
        </div>
      </button>

      {expanded && (
        <div className="child-body">
          {/* Badges */}
          {child.badges?.length > 0 && (
            <div className="child-section">
              <h4>🏆 Badges</h4>
              <div className="child-badges">
                {child.badges.map((b, i) => (
                  <BadgeCard key={i} emoji={b.emoji || '🏅'} name={b.name} description={b.description} />
                ))}
              </div>
            </div>
          )}

          {/* Stats row */}
          <div className="child-stats-row">
            <div className="child-stat-box">
              <span className="stat-big">{progressData?.lessons_this_week ?? child.lessons_this_week ?? 0}</span>
              <span className="stat-desc">Lessons this week</span>
            </div>
            <div className="child-stat-box">
              <span className="stat-big">{quizAvg}%</span>
              <span className="stat-desc">Quiz average</span>
            </div>
          </div>

          {/* Progress chart */}
          <div className="child-section">
            <h4>📊 Weekly Progress</h4>
            <SimpleBarChart data={weekly} />
          </div>

          {/* AI Chat history */}
          <div className="child-section">
            <button className="chat-toggle-btn" onClick={() => setChatOpen(!chatOpen)}>
              💬 AI Chat History {chatOpen ? '(hide)' : '(show)'}
            </button>
            {chatOpen && (
              <div className="chat-history">
                {progressData?.chat_history?.length > 0 ? (
                  progressData.chat_history.map((q, i) => (
                    <div key={i} className="chat-entry">
                      <span className="chat-q">Q: {q.question}</span>
                      <span className="chat-time">{new Date(q.timestamp).toLocaleString()}</span>
                    </div>
                  ))
                ) : (
                  <p className="no-data">No chat history yet 💭</p>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ParentDashboard() {
  const [children, setChildren] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getChildren()
      .then((r) => setChildren(r.data || []))
      .catch(() => setChildren([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner message="Loading your family's data..." />;

  return (
    <div className="pdash">
      <h1>👨‍👩‍👧 Parent Dashboard</h1>
      <p className="pdash-sub">Here's how your child is doing!</p>

      {children.length === 0 ? (
        <div className="pdash-empty">
          <p>No linked children found.</p>
          <p>Make sure your child registered with your email as their parent email! 📧</p>
        </div>
      ) : (
        <div className="child-list">
          {children.map((child) => (
            <ChildCard key={child.id} child={child} />
          ))}
        </div>
      )}

      <style>{`
        .pdash { max-width: 800px; margin: 0 auto; }
        .pdash h1 { font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem; }
        .pdash-sub { color: var(--text-light); margin-bottom: 1.5rem; }
        .pdash-empty { text-align: center; padding: 3rem; color: var(--text-light); background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow); }
        .child-list { display: flex; flex-direction: column; gap: 1rem; }
        .child-card { background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow); overflow: hidden; }
        .child-header {
          width: 100%; display: flex; justify-content: space-between; align-items: center;
          padding: 1.125rem 1.25rem; background: none; border: none; cursor: pointer; gap: 1rem;
        }
        .child-header:hover { background: var(--bg); }
        .child-info { display: flex; align-items: center; gap: 0.75rem; }
        .child-avatar { font-size: 2rem; }
        .child-name { font-weight: 700; font-size: 1rem; }
        .child-email { font-size: 0.78rem; color: var(--text-light); }
        .child-stats { display: flex; align-items: center; gap: 0.75rem; flex-shrink: 0; }
        .child-stat { font-weight: 700; font-size: 0.85rem; color: var(--primary); }
        .child-toggle { color: var(--text-light); font-size: 0.7rem; }
        .child-body { padding: 0.5rem 1.25rem 1.25rem; border-top: 1px solid var(--border); display: flex; flex-direction: column; gap: 1.25rem; }
        .child-section h4 { font-weight: 700; margin-bottom: 0.625rem; font-size: 0.9rem; }
        .child-badges { display: flex; flex-wrap: wrap; gap: 0.5rem; }
        .child-stats-row { display: flex; gap: 1rem; }
        .child-stat-box {
          flex: 1; background: var(--bg); border-radius: var(--radius);
          padding: 0.875rem; text-align: center;
        }
        .stat-big { font-size: 1.75rem; font-weight: 800; color: var(--primary); display: block; }
        .stat-desc { font-size: 0.78rem; color: var(--text-light); font-weight: 600; }
        .bar-chart { display: flex; flex-direction: column; gap: 0.5rem; }
        .bar-row { display: flex; align-items: center; gap: 0.75rem; }
        .bar-label { font-size: 0.8rem; color: var(--text-light); min-width: 70px; }
        .bar-track { flex: 1; height: 10px; background: var(--bg); border-radius: 5px; overflow: hidden; }
        .bar-fill { height: 100%; background: var(--primary); border-radius: 5px; transition: width 0.5s ease; }
        .bar-count { font-size: 0.78rem; font-weight: 700; min-width: 20px; text-align: right; }
        .chat-toggle-btn {
          background: none; border: 2px solid var(--border); border-radius: var(--radius);
          padding: 0.4rem 0.875rem; font-weight: 700; font-size: 0.85rem; cursor: pointer;
          color: var(--text);
        }
        .chat-toggle-btn:hover { border-color: var(--primary); }
        .chat-history { margin-top: 0.75rem; display: flex; flex-direction: column; gap: 0.5rem; }
        .chat-entry {
          display: flex; justify-content: space-between; align-items: flex-start;
          padding: 0.625rem 0.875rem; background: var(--bg); border-radius: var(--radius);
        }
        .chat-q { font-size: 0.85rem; font-weight: 600; }
        .chat-time { font-size: 0.72rem; color: var(--text-light); }
        .no-data { color: var(--text-light); font-size: 0.85rem; padding: 0.5rem 0; }
        @media (max-width: 600px) {
          .child-header { flex-direction: column; align-items: flex-start; }
          .child-stats { flex-wrap: wrap; }
        }
      `}</style>
    </div>
  );
}
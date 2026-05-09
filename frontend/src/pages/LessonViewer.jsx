import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getLesson, completeLesson } from '../api';
import RAPCard from '../components/RAPCard';
import MovementBreak from '../components/MovementBreak';
import BadgeCard from '../components/BadgeCard';
import LoadingSpinner from '../components/LoadingSpinner';

function renderContent(text) {
  if (!text) return '';
  return text
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li><strong>$1.</strong> $2</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\|(.+)\|/g, (match) => {
      const cells = match.split('|').filter(Boolean);
      const isHeader = cells.some((c) => c.trim().match(/^-+$/));
      if (isHeader) return '';
      return '<tr>' + cells.map((c) => `<td>${c.trim()}</td>`).join('') + '</tr>';
    })
    .replace(/(<tr>.*<\/tr>)/s, '<table>$1</table>')
    .replace(/<\/tr><tr>/g, '')
    .replace(/^(?!<[hlt])/gm, '')
    .replace(/\n/g, '<br/>');
}

export default function LessonViewer() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [showBreak, setShowBreak] = useState(false);
  const [showRAP, setShowRAP] = useState(true);
  const [earnedBadge, setEarnedBadge] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [pointsEarned, setPointsEarned] = useState(0);
  const breakTimerRef = useRef(null);
  const contentRef = useRef(null);

  useEffect(() => {
    loadLesson();
    return () => clearTimeout(breakTimerRef.current);
  }, [id]);

  const loadLesson = async () => {
    try {
      const res = await getLesson(id);
      setLesson(res.data);
      if (res.data.completed) setCompleted(true);
      scheduleBreak(res.data.duration_minutes || 10);
    } catch {
      navigate('/lessons');
    } finally {
      setLoading(false);
    }
  };

  const scheduleBreak = (durationMinutes) => {
    clearTimeout(breakTimerRef.current);
    const ms = Math.max(30000, durationMinutes * 60 * 500); // half the lesson duration or 30s
    breakTimerRef.current = setTimeout(() => setShowBreak(true), ms);
  };

  const handleComplete = async () => {
    setCompleting(true);
    try {
      const res = await completeLesson(id);
      setCompleted(true);
      setPointsEarned(res.data.points_earned || 10);
      if (res.data.badge) {
        setEarnedBadge(res.data.badge);
      }
    } catch {
      setCompleted(true);
    } finally {
      setCompleting(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading lesson..." />;
  if (!lesson) return null;

  return (
    <div className="lv-wrap">
      {showBreak && <MovementBreak onDismiss={() => setShowBreak(false)} />}

      <div className="lv-layout">
        <div className="lv-content">
          <button className="lv-back" onClick={() => navigate('/lessons')}>← Back to Lessons</button>

          <div className="lv-header">
            <h1 className="lv-title">{lesson.title}</h1>
            <p className="lv-meta">⏱ {lesson.duration_minutes || 10} min read</p>
          </div>

          <div
            ref={contentRef}
            className="lv-body"
            dangerouslySetInnerHTML={{ __html: renderContent(lesson.content || '') }}
          />

          {completed ? (
            <div className="lv-completed">
              <p>✅ You've completed this lesson!</p>
              {pointsEarned > 0 && <p>⭐ You earned <strong>{pointsEarned} points</strong>!</p>}
              <button className="lv-quiz-btn" onClick={() => navigate('/lessons')}>Back to Lessons</button>
            </div>
          ) : (
            <button className="lv-complete-btn" onClick={handleComplete} disabled={completing}>
              {completing ? 'Saving...' : '✅ Complete Lesson'}
            </button>
          )}

          {earnedBadge && (
            <div className="lv-badge-popup">
              <BadgeCard emoji={earnedBadge.emoji} name={earnedBadge.name} description={earnedBadge.description} isNew />
            </div>
          )}
        </div>

        <div className="lv-sidebar">
          <button className="lv-rap-toggle" onClick={() => setShowRAP(!showRAP)}>
            {showRAP ? 'Hide RAP' : 'Show RAP'}
          </button>
          {showRAP && <RAPCard />}
        </div>
      </div>

      <style>{`
        .lv-wrap { max-width: 1100px; margin: 0 auto; }
        .lv-layout { display: flex; gap: 1.5rem; align-items: flex-start; }
        .lv-content { flex: 1; min-width: 0; }
        .lv-sidebar { width: 260px; flex-shrink: 0; position: sticky; top: 80px; }
        .lv-back {
          background: none; border: none;
          color: var(--primary); font-weight: 600;
          cursor: pointer; font-size: 0.9rem;
          margin-bottom: 1rem; padding: 0;
        }
        .lv-back:hover { text-decoration: underline; }
        .lv-header { margin-bottom: 1.5rem; }
        .lv-title { font-size: 1.75rem; font-weight: 800; color: var(--text); margin-bottom: 0.35rem; }
        .lv-meta { color: var(--text-light); font-size: 0.85rem; }
        .lv-body {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 2rem;
          box-shadow: var(--shadow);
          line-height: 1.8;
          font-size: 1rem;
        }
        .lv-body h1 { font-size: 1.5rem; margin: 1.5rem 0 0.75rem; color: var(--primary); }
        .lv-body h2 { font-size: 1.25rem; margin: 1.25rem 0 0.6rem; }
        .lv-body h3 { font-size: 1.1rem; margin: 1rem 0 0.5rem; }
        .lv-body p { margin-bottom: 0.75rem; }
        .lv-body li { margin-left: 1.25rem; margin-bottom: 0.35rem; }
        .lv-body table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
        .lv-body td { padding: 0.5rem 0.75rem; border: 1px solid var(--border); }
        .lv-body tr:first-child td { background: var(--bg); font-weight: 700; }
        .lv-body strong { color: var(--primary); }
        .lv-complete-btn {
          width: 100%; margin-top: 1.5rem;
          padding: 1rem;
          background: var(--primary);
          color: white;
          border: none;
          border-radius: var(--radius);
          font-size: 1rem;
          font-weight: 800;
          cursor: pointer;
          transition: all 0.2s;
        }
        .lv-complete-btn:hover:not(:disabled) { background: var(--primary-dark); transform: translateY(-1px); }
        .lv-complete-btn:disabled { opacity: 0.7; cursor: not-allowed; }
        .lv-completed {
          margin-top: 1.5rem;
          padding: 1.25rem;
          background: #D1FAE5;
          border-radius: var(--radius-lg);
          text-align: center;
        }
        .lv-completed p { margin-bottom: 0.5rem; font-size: 0.95rem; }
        .lv-quiz-btn {
          margin-top: 0.75rem;
          padding: 0.6rem 1.5rem;
          background: var(--secondary);
          color: white;
          border: none;
          border-radius: var(--radius);
          font-weight: 700;
          cursor: pointer;
        }
        .lv-badge-popup { margin-top: 1rem; }
        .lv-rap-toggle {
          width: 100%; margin-bottom: 0.5rem;
          padding: 0.5rem;
          background: var(--card);
          border: 2px solid var(--border);
          border-radius: var(--radius);
          font-weight: 700;
          font-size: 0.85rem;
          cursor: pointer;
        }
        .lv-rap-toggle:hover { border-color: var(--primary); }
        @media (max-width: 768px) {
          .lv-layout { flex-direction: column; }
          .lv-sidebar { width: 100%; position: static; }
        }
      `}</style>
    </div>
  );
}
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSubjects, getUnits, getUnitLessons } from '../api';
import ProgressBar from '../components/ProgressBar';
import LoadingSpinner from '../components/LoadingSpinner';

export default function LessonsPage() {
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState([]);
  const [activeSubject, setActiveSubject] = useState(null);
  const [units, setUnits] = useState([]);
  const [expandedUnit, setExpandedUnit] = useState(null);
  const [unitLessons, setUnitLessons] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const res = await getSubjects();
      setSubjects(res.data || []);
      if (res.data?.length > 0) {
        setActiveSubject(res.data[0]);
      }
    } catch {
      setSubjects([]);
    } finally {
      setLoading(false);
    }
  };

  const loadUnits = async (subject) => {
    setActiveSubject(subject);
    setExpandedUnit(null);
    setUnitLessons({});
    try {
      const res = await getUnits(subject.id);
      setUnits(res.data || []);
    } catch {
      setUnits([]);
    }
  };

  const toggleUnit = async (unit) => {
    if (expandedUnit === unit.id) {
      setExpandedUnit(null);
      return;
    }
    setExpandedUnit(unit.id);
    if (!unitLessons[unit.id]) {
      try {
        const res = await getUnitLessons(unit.id);
        setUnitLessons((prev) => ({ ...prev, [unit.id]: res.data || [] }));
      } catch {
        setUnitLessons((prev) => ({ ...prev, [unit.id]: [] }));
      }
    }
  };

  if (loading) return <LoadingSpinner message="Loading lessons..." />;

  return (
    <div className="lpage">
      <h1 className="lpage-title">📖 Lessons</h1>

      <div className="subject-tabs">
        {subjects.map((s) => (
          <button
            key={s.id}
            className={`subj-tab ${activeSubject?.id === s.id ? 'active' : ''}`}
            onClick={() => loadUnits(s)}
          >
            <span>{s.name === 'Math' ? '🔢' : '🔬'}</span>
            {s.name}
          </button>
        ))}
      </div>

      {units.length === 0 && activeSubject && (
        <p className="lpage-empty">No units yet for {activeSubject.name}. Check back soon! 🎉</p>
      )}

      <div className="unit-list">
        {units.map((unit) => {
          const lessons = unitLessons[unit.id] || [];
          const completedCount = lessons.filter((l) => l.completed).length;
          const pct = lessons.length > 0 ? (completedCount / lessons.length) * 100 : 0;

          return (
            <div key={unit.id} className="unit-card">
              <button className="unit-header" onClick={() => toggleUnit(unit)}>
                <div className="unit-info">
                  <h3 className="unit-title">{unit.title}</h3>
                  <p className="unit-meta">
                    📅 Weeks {unit.week_start}–{unit.week_end} &nbsp;·&nbsp;
                    📚 {unit.lesson_count || lessons.length} lessons
                  </p>
                </div>
                <div className="unit-right">
                  <ProgressBar percent={pct} subject={activeSubject?.name?.toLowerCase()} />
                  <span className="unit-toggle">{expandedUnit === unit.id ? '▲' : '▼'}</span>
                </div>
              </button>

              {expandedUnit === unit.id && (
                <div className="unit-lessons">
                  {lessons.length === 0 && <p className="lpage-empty">Loading lessons...</p>}
                  {lessons.map((lesson, idx) => {
                    const isLocked = idx > 0 && !lessons[idx - 1]?.completed;
                    return (
                      <div key={lesson.id} className={`lesson-row ${lesson.completed ? 'done' : ''} ${isLocked ? 'locked' : ''}`}>
                        <div className="lesson-row-left">
                          <span className="lesson-status-icon">
                            {isLocked ? '🔒' : lesson.completed ? '✅' : '⬜'}
                          </span>
                          <div>
                            <p className="lesson-title">{lesson.title}</p>
                            <p className="lesson-duration">⏱ {lesson.duration_minutes || 10} min</p>
                          </div>
                        </div>
                        {!isLocked && (
                          <button
                            className="lesson-start-btn"
                            onClick={() => navigate(`/lesson/${lesson.id}`)}
                          >
                            {lesson.completed ? '🔄 Review' : '▶ Start'}
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <style>{`
        .lpage { max-width: 800px; margin: 0 auto; }
        .lpage-title { font-size: 1.5rem; font-weight: 800; margin-bottom: 1.25rem; }
        .subject-tabs { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
        .subj-tab {
          display: flex; align-items: center; gap: 0.5rem;
          padding: 0.6rem 1.25rem;
          border: 2px solid var(--border);
          border-radius: var(--radius);
          background: var(--card);
          font-weight: 700;
          font-size: 0.95rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .subj-tab.active { border-color: var(--primary); background: #EEF2FF; color: var(--primary); }
        .subj-tab:hover:not(.active) { border-color: var(--primary-light); }
        .unit-list { display: flex; flex-direction: column; gap: 1rem; }
        .unit-card { background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow); overflow: hidden; }
        .unit-header {
          width: 100%;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1.125rem 1.25rem;
          background: none;
          border: none;
          cursor: pointer;
          text-align: left;
          gap: 1rem;
        }
        .unit-header:hover { background: var(--bg); }
        .unit-info { flex: 1; }
        .unit-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 0.25rem; }
        .unit-meta { font-size: 0.8rem; color: var(--text-light); }
        .unit-right { display: flex; align-items: center; gap: 0.75rem; flex-shrink: 0; }
        .unit-toggle { color: var(--text-light); font-size: 0.75rem; }
        .unit-right > div { min-width: 100px; }
        .unit-lessons { border-top: 1px solid var(--border); padding: 0.5rem; }
        .lesson-row {
          display: flex; align-items: center; justify-content: space-between;
          padding: 0.75rem 0.875rem;
          border-radius: var(--radius);
          transition: background 0.15s;
        }
        .lesson-row:not(.locked):hover { background: var(--bg); }
        .lesson-row.locked { opacity: 0.55; }
        .lesson-row.done .lesson-title { color: var(--text-light); }
        .lesson-row-left { display: flex; align-items: center; gap: 0.75rem; }
        .lesson-status-icon { font-size: 1.1rem; flex-shrink: 0; }
        .lesson-title { font-weight: 600; font-size: 0.9rem; }
        .lesson-duration { font-size: 0.75rem; color: var(--text-light); }
        .lesson-start-btn {
          padding: 0.4rem 0.875rem;
          background: var(--primary);
          color: white;
          border: none;
          border-radius: var(--radius);
          font-weight: 700;
          font-size: 0.8rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .lesson-start-btn:hover { background: var(--primary-dark); }
        .lpage-empty { color: var(--text-light); padding: 1rem 0; font-size: 0.9rem; text-align: center; }
      `}</style>
    </div>
  );
}
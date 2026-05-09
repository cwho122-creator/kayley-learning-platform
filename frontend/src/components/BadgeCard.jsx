import React from 'react';

export default function BadgeCard({ emoji, name, description, isNew }) {
  return (
    <div className={`bc-card ${isNew ? 'bc-new' : ''}`}>
      <div className="bc-emoji">{emoji}</div>
      <div className="bc-info">
        <p className="bc-name">{name}</p>
        <p className="bc-desc">{description}</p>
      </div>
      {isNew && <span className="bc-new-badge">✨ NEW!</span>}
      <style>{`
        .bc-card {
          display: flex; align-items: center; gap: 0.875rem;
          padding: 0.875rem;
          background: var(--card);
          border-radius: var(--radius-lg);
          border: 2px solid var(--border);
          position: relative;
        }
        .bc-card.bc-new {
          border-color: #FDE047;
          box-shadow: 0 0 16px rgba(253, 224, 71, 0.4);
        }
        .bc-emoji { font-size: 2rem; flex-shrink: 0; }
        .bc-info { flex: 1; min-width: 0; }
        .bc-name { font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem; }
        .bc-desc { font-size: 0.78rem; color: var(--text-light); }
        .bc-new-badge {
          position: absolute; top: -8px; right: -8px;
          background: #F59E0B; color: white;
          font-size: 0.65rem; font-weight: 800;
          padding: 0.2rem 0.5rem;
          border-radius: 20px;
        }
      `}</style>
    </div>
  );
}
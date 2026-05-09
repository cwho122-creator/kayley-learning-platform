import React from 'react';

export default function ProgressBar({ percent, subject }) {
  const color = subject === 'science' ? 'var(--secondary)' : 'var(--primary)';
  return (
    <div className="pb-wrap">
      <div className="pb-track">
        <div
          className="pb-fill"
          style={{ width: `${Math.min(100, Math.max(0, percent))}%`, background: color }}
        />
      </div>
      <span className="pb-label">{Math.round(percent)}%</span>
      <style>{`
        .pb-wrap { display: flex; align-items: center; gap: 0.5rem; }
        .pb-track {
          flex: 1; height: 10px;
          background: var(--bg);
          border-radius: 5px;
          overflow: hidden;
        }
        .pb-fill {
          height: 100%;
          border-radius: 5px;
          transition: width 0.6s ease;
        }
        .pb-label { font-size: 0.78rem; font-weight: 700; color: var(--text-light); min-width: 32px; text-align: right; }
      `}</style>
    </div>
  );
}
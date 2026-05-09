import React from 'react';

export default function LoadingSpinner({ message }) {
  return (
    <div className="ls-wrap">
      <div className="ls-spinner" />
      {message && <p className="ls-message">{message}</p>}
      <style>{`
        .ls-wrap { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 2rem; }
        .ls-spinner {
          width: 44px; height: 44px;
          border: 4px solid var(--border);
          border-top-color: var(--primary);
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
        .ls-message { color: var(--text-light); font-size: 0.9rem; }
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
}
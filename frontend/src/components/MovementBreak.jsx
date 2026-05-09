import React from 'react';

const MESSAGES = [
  { text: '🧘 Time for a movement break! Stretch your arms high!', emoji: '🧘‍♀️' },
  { text: '🏃 Lets get moving! Jump 10 times or dance it out!', emoji: '💃' },
  { text: '🧠 Brains work better after moving! Touch your toes 5 times!', emoji: '🦵' },
  { text: '🌟 Take a break! Walk around the room and get some water!', emoji: '💧' },
  { text: '🎉 Movement break! Do 5 big arm circles each way!', emoji: '🏃‍♀️' },
];

let messageIndex = 0;

export default function MovementBreak({ onDismiss }) {
  const msg = MESSAGES[messageIndex % MESSAGES.length];
  messageIndex++;

  return (
    <div className="mb-overlay">
      <div className="mb-modal">
        <div className="mb-emoji">{msg.emoji}</div>
        <h2 className="mb-title">Movement Break!</h2>
        <p className="mb-text">{msg.text}</p>
        <button className="mb-btn" onClick={onDismiss}>
          I'm done! ✅
        </button>
      </div>
      <style>{`
        .mb-overlay {
          position: fixed;
          inset: 0;
          background: rgba(0,0,0,0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 999;
          animation: fadeIn 0.3s ease;
        }
        .mb-modal {
          background: var(--card);
          border-radius: var(--radius-lg);
          padding: 2.5rem 2rem;
          text-align: center;
          max-width: 380px;
          width: 90%;
          box-shadow: var(--shadow-lg);
          animation: slideUp 0.4s ease;
        }
        .mb-emoji { font-size: 4rem; margin-bottom: 0.5rem; animation: bounce 0.6s infinite alternate; }
        .mb-title { color: var(--primary); margin-bottom: 0.75rem; font-size: 1.5rem; }
        .mb-text { color: var(--text-light); margin-bottom: 1.5rem; font-size: 1rem; line-height: 1.5; }
        .mb-btn {
          background: var(--primary);
          color: white;
          border: none;
          border-radius: var(--radius);
          padding: 0.75rem 2rem;
          font-size: 1rem;
          font-weight: 700;
          cursor: pointer;
          transition: transform 0.15s, background 0.2s;
        }
        .mb-btn:hover { background: var(--primary-dark); transform: scale(1.03); }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes bounce { from { transform: scale(1); } to { transform: scale(1.15) rotate(-5deg); } }
      `}</style>
    </div>
  );
}
import React, { useState, useRef, useEffect } from 'react';
import { askAI } from '../api';

function SimpleMarkdown({ text }) {
  if (!text) return null;
  const lines = text.split('\n');
  return (
    <div className="ai-msg-text">
      {lines.map((line, i) => {
        const bold = line.replace(/\*\*(.+?)\*\*/g, '||BOLD||$1||END||');
        const parts = bold.split('||END||');
        return (
          <p key={i}>
            {parts.map((p, j) => {
              if (p.startsWith('||BOLD||')) {
                return <strong key={j}>{p.replace('||BOLD||', '')}</strong>;
              }
              return <span key={j}>{p}</span>;
            })}
          </p>
        );
      })}
    </div>
  );
}

export default function AITutorPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [understood, setUnderstood] = useState(null);
  const [pendingFollowup, setPendingFollowup] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = async (text) => {
    if (!text.trim() || loading) return;
    const userMsg = { role: 'user', text };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);
    setUnderstood(null);
    setPendingFollowup(false);

    try {
      const res = await askAI({ question: text, chat_history: messages.map((m) => ({ role: m.role, content: m.text })) });
      const aiText = res.data?.answer || res.data?.response || "I'm not sure about that — try asking differently! 🤔";
      const relatedLessons = res.data?.related_lessons || [];
      setMessages((m) => [
        ...m,
        { role: 'ai', text: aiText, lessons: relatedLessons, showUnderstand: true },
      ]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: 'ai', text: "Oops! Something went wrong. Try again! 💡", showUnderstand: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    send(input);
  };

  const handleUnderstand = (ok) => {
    setUnderstood(ok);
    if (!ok) {
      setPendingFollowup(true);
      setMessages((m) => [...m, { role: 'ai', text: "No worries! Which part was confusing? Tell me and I'll explain it differently! 💬" }]);
    }
  };

  const clearChat = () => setMessages([]);

  return (
    <div className="ai-page">
      <div className="ai-header">
        <h1>🤖 AI Tutor</h1>
        <button className="ai-clear-btn" onClick={clearChat}>🗑️ Clear Chat</button>
      </div>

      <div className="ai-chat">
        {messages.length === 0 && (
          <div className="ai-empty">
            <p>👋 Hi! I'm your AI tutor.</p>
            <p>Ask me anything about your lessons — I'll keep it short and simple! ✨</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`ai-msg ai-${msg.role}`}>
            <div className="ai-avatar">{msg.role === 'ai' ? '🤖' : '🧒'}</div>
            <div className="ai-bubble">
              <SimpleMarkdown text={msg.text} />
              {msg.role === 'ai' && msg.lessons?.length > 0 && (
                <div className="ai-lessons">
                  <p>📚 Related lessons:</p>
                  {msg.lessons.map((l, j) => (
                    <a key={j} href={`/lesson/${l.id}`} className="ai-lesson-link">📖 {l.title}</a>
                  ))}
                </div>
              )}
              {msg.role === 'ai' && msg.showUnderstand && messages.indexOf(msg) === messages.length - 1 && !pendingFollowup && (
                <div className="ai-understand-btns">
                  <button className="ai-understand-btn ok" onClick={() => handleUnderstand(true)}>Yes ✅</button>
                  <button className="ai-understand-btn no" onClick={() => handleUnderstand(false)}>No ❌</button>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="ai-msg ai-ai">
            <div className="ai-avatar">🤖</div>
            <div className="ai-bubble typing">Thinking... 💭</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="ai-input-area" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask your question here..."
          className="ai-input"
          disabled={loading}
        />
        <button type="submit" className="ai-send-btn" disabled={loading || !input.trim()}>
          Send 🚀
        </button>
      </form>

      <style>{`
        .ai-page { display: flex; flex-direction: column; height: calc(100vh - 80px); max-width: 800px; margin: 0 auto; }
        .ai-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
        .ai-header h1 { font-size: 1.5rem; font-weight: 800; }
        .ai-clear-btn {
          padding: 0.4rem 0.875rem;
          background: var(--card);
          border: 2px solid var(--border);
          border-radius: var(--radius);
          font-weight: 600;
          font-size: 0.85rem;
          cursor: pointer;
        }
        .ai-chat {
          flex: 1;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 1rem;
          padding: 1rem 0;
          min-height: 0;
        }
        .ai-empty {
          text-align: center;
          color: var(--text-light);
          padding: 2rem;
          font-size: 0.95rem;
        }
        .ai-msg { display: flex; gap: 0.75rem; align-items: flex-start; }
        .ai-ai { flex-direction: row; }
        .ai-user { flex-direction: row-reverse; }
        .ai-avatar {
          width: 36px; height: 36px;
          border-radius: 50%;
          background: var(--bg);
          display: flex; align-items: center; justify-content: center;
          font-size: 1.1rem;
          flex-shrink: 0;
        }
        .ai-ai .ai-avatar { background: #EEF2FF; }
        .ai-bubble {
          max-width: 75%;
          padding: 0.875rem 1.125rem;
          border-radius: var(--radius-lg);
          line-height: 1.7;
          font-size: 0.95rem;
        }
        .ai-ai .ai-bubble { background: var(--card); box-shadow: var(--shadow); }
        .ai-user .ai-bubble { background: var(--primary); color: white; }
        .ai-msg-text p { margin-bottom: 0.35rem; }
        .ai-msg-text p:last-child { margin-bottom: 0; }
        .ai-msg-text strong { color: var(--primary); }
        .ai-user .ai-msg-text strong { color: #C7D2FE; }
        .ai-lessons { margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border); }
        .ai-lessons p { font-size: 0.78rem; color: var(--text-light); font-weight: 600; margin-bottom: 0.35rem; }
        .ai-lesson-link { display: block; font-size: 0.82rem; color: var(--primary); font-weight: 600; }
        .ai-understand-btns { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
        .ai-understand-btn {
          padding: 0.4rem 0.875rem;
          border-radius: var(--radius);
          border: 2px solid;
          font-weight: 700;
          font-size: 0.82rem;
          cursor: pointer;
        }
        .ai-understand-btn.ok { border-color: var(--success); color: var(--success); background: transparent; }
        .ai-understand-btn.no { border-color: var(--error); color: var(--error); background: transparent; }
        .ai-understand-btn:hover { opacity: 0.8; }
        .ai-input-area {
          display: flex;
          gap: 0.75rem;
          padding: 0.75rem 0;
          border-top: 1px solid var(--border);
          flex-shrink: 0;
        }
        .ai-input {
          flex: 1;
          padding: 0.875rem 1rem;
          border: 2px solid var(--border);
          border-radius: var(--radius);
          font-size: 0.95rem;
          background: var(--card);
        }
        .ai-input:focus { outline: none; border-color: var(--primary); }
        .ai-send-btn {
          padding: 0.875rem 1.5rem;
          background: var(--primary);
          color: white;
          border: none;
          border-radius: var(--radius);
          font-weight: 700;
          cursor: pointer;
          transition: all 0.2s;
        }
        .ai-send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .ai-send-btn:hover:not(:disabled) { background: var(--primary-dark); }
        .typing { color: var(--text-light); font-style: italic; }
      `}</style>
    </div>
  );
}
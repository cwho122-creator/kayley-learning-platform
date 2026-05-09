# Kayley's ADHD-Friendly Learning Platform

A personalized learning platform for Kayley, a 12-year-old student with ADHD studying IB MYP Year 8 at South Island School, Hong Kong.

## Features

- **📝 RAP Strategy Cards** - Step-by-step question interpretation guide
- **📖 Chunked Mini-Lessons** - 5-10 minute lessons with movement breaks
- **📊 Visual Progress Dashboard** - Track points, streaks, and badges
- **🧮 Interactive Quizzes** - Max 5 questions per session with instant feedback
- **🔢 Math Tools** - Desmos/GeoGebra integration for visual algebra
- **🧬 Science Concept Maps** - Visual topic links
- **🎮 Gamification** - Points, badges, and streaks
- **🤖 AI Tutor** - Ask questions anytime (powered by Groq)
- **👨‍👩 Parent Dashboard** - Monitor progress and chat history
- **🏃 Movement Break Reminders** - Built-in stretch breaks

## Tech Stack

- **Backend:** Python + FastAPI + SQLAlchemy
- **Frontend:** React + Vite
- **Database:** PostgreSQL
- **AI:** Groq LLM API (free tier available)

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (local or cloud)
- Groq API key (free at groq.com)

### Backend Setup

```bash
cd backend
cp env.example .env
# Edit .env with your DATABASE_URL and GROQ_API_KEY
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Database

The database will auto-create tables on first run. Content (lessons, quizzes) will be seeded automatically.

## Deployment

### Backend (Railway/Render/Fly.io)

1. Push to GitHub
2. Connect repo to chosen platform
3. Set environment variables:
   - `DATABASE_URL` - PostgreSQL connection string
   - `GROQ_API_KEY` - Free API key from groq.com
4. Deploy

### Frontend (Vercel/Netlify)

1. Set API URL to your backend endpoint
2. Deploy

## User Accounts

- **Student:** Kayley (or other linked student)
- **Parent:** Parent account to monitor progress

## ADHD Adaptations

- One concept per lesson
- Color-coded notation (blue=positive, red=negative)
- 3-minute movement breaks every 7-10 minutes
- Max 3 steps per checklist
- Short, encouraging AI responses
- Visual progress tracking

## Subjects Covered

### Math (MYP Year 8)
- Unit 1: Algebraic Expressions & Directed Numbers
- Unit 2: Patterns, Relations & Graphing
- Unit 3: Measurement (Area, Perimeter, Volume)
- Unit 4: Statistics & Geometry

### Science (MYP Year 8)
- Cells and Life
- Ecosystems
- Chemical Reactions
- Forces and Energy
- Electricity and Circuits

## License

Private - For Kayley's learning only.

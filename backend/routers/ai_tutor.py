"""AI Tutor router - chat with an AI tutor."""
import os
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database import get_db
from backend.models import User, StudentProfile, ChatSession, ChatMessage
from backend.schemas import ChatAskResponse, ChatMessageResponse, ChatSessionResponse
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Tutor"])

# MiniMax API setup (OpenAI-compatible)
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"
MINIMAX_MODEL = "MiniMax-Text-01"

MATH_TOPICS = [
    "algebraic expressions", "directed numbers", "equations", 
    "linear relationships", "graphing", "area", "perimeter",
    "volume", "surface area", "statistics", "probability"
]

SCIENCE_TOPICS = [
    "cells", "organisms", "ecosystems", "chemical reactions",
    "atoms", "molecules", "forces", "motion", "energy",
    "electricity", "circuits"
]

ADHP_PROMPTS = """
You are a friendly, patient AI tutor for Kayley, a 12-year-old girl with ADHD studying IB MYP Year 8 in Hong Kong.
- Keep responses VERY SHORT (1-3 sentences max)
- Use simple words a 7th grader understands
- Use emojis to make it fun
- Break complex ideas into tiny steps
- Always be encouraging and positive
- If she doesn't understand, ask what part specifically is confusing
- ADHD-friendly: no long walls of text, use bullets and emojis
- Link to related lessons when relevant
- Be warm and supportive like a friendly older sister
"""


def build_system_prompt():
    return f"""{ADHP_PROMPTS}

Her current subjects are:
- Math (Year 8 MYP): algebraic expressions, directed numbers, equations, linear relationships, graphing, area, perimeter, volume, statistics
- Science (Year 8 MYP): cells, ecosystems, chemical reactions, forces, energy, electricity

When she asks about a topic, explain simply and link to the relevant lesson if she needs to study more."""


def call_minimax(system: str, user_message: str) -> str:
    """Call MiniMax API for AI response (OpenAI-compatible)."""
    if not MINIMAX_API_KEY:
        return "AI tutor is not configured yet. Please ask your parent to set up the API key!"
    
    try:
        import urllib.request
        import urllib.error
        
        url = f"{MINIMAX_BASE_URL}/chat/completions"
        data = {
            "model": MINIMAX_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {MINIMAX_API_KEY}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]
    
    except Exception as e:
        return f"Sorry Kayley! I'm having trouble thinking right now. Try again in a moment! 😅\n\n(Error: {str(e)[:100]})"


def find_related_lesson(db: Session, message: str) -> dict | None:
    """Find a lesson related to the user's question."""
    message_lower = message.lower()
    
    # Simple keyword matching
    for topic in MATH_TOPICS + SCIENCE_TOPICS:
        if topic in message_lower:
            from backend.models import Lesson
            lesson = db.query(Lesson).filter(
                Lesson.title.ilike(f"%{topic}%")
            ).first()
            
            if lesson:
                return {"id": lesson.id, "title": lesson.title}
    
    return None


@router.post("/tutor", response_model=ChatAskResponse)
def ask_tutor(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message to the AI tutor."""
    if current_user.role not in ["student", "parent"]:
        raise HTTPException(status_code=403, detail="Only students and parents can use the tutor")
    
    # Get or create session
    session_id = request.session_id
    if session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        ).first()
    else:
        # Create new session
        session = ChatSession(
            user_id=current_user.id,
            title=f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = session.id
    
    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        sender="user",
        content=request.message
    )
    db.add(user_msg)
    db.commit()
    
    # Build prompt and call AI
    system_prompt = build_system_prompt()
    user_name = current_user.full_name if current_user.role == "student" else "Kayley"
    full_prompt = f"The student ({user_name}) asks: {request.message}"
    
    ai_response = call_minimax(system_prompt, full_prompt)
    
    # Save AI response
    ai_msg = ChatMessage(
        session_id=session_id,
        sender="ai",
        content=ai_response
    )
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)
    
    # Find related lesson
    related = find_related_lesson(db, request.message)
    
    return ChatAskResponse(
        session_id=session_id,
        message=ChatMessageResponse.model_validate(ai_msg),
        response=ai_response,
        related_lesson=related
    )


@router.get("/history", response_model=list)
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all chat sessions for current user."""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(desc(ChatSession.updated_at)).limit(20).all()
    
    return [
        ChatSessionResponse(
            id=s.id,
            title=s.title,
            created_at=s.created_at,
            updated_at=s.updated_at,
            messages=[
                ChatMessageResponse(
                    id=m.id,
                    sender=m.sender,
                    content=m.content,
                    created_at=m.created_at
                )
                for m in s.messages
            ]
        )
        for s in sessions
    ]


@router.delete("/history/{session_id}")
def delete_chat_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a chat session."""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    
    return {"success": True}

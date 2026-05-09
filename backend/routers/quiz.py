"""Quiz router - quiz management and attempts."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from backend.database import get_db
from backend.models import (
    User, Quiz, QuizQuestion, QuizAttempt, QuestionAttempt,
    StudentProfile, Badge, ProgressRecord
)
from backend.schemas import QuizResponse, QuizQuestionResponse, QuizSubmissionRequest, QuizResultResponse
from backend.routers.auth import get_current_user
from backend.routers.lessons import check_and_award_badges

router = APIRouter(prefix="/quiz", tags=["Quizzes"])


@router.get("/lesson/{lesson_id}", response_model=QuizResponse)
def get_quiz_by_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get quiz for a specific lesson (without revealing answers)."""
    quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return quiz


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get a specific quiz."""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.post("/start/{quiz_id}", response_model=dict)
def start_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a new quiz attempt."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can take quizzes")
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Create new attempt
    attempt = QuizAttempt(
        student_id=student.id,
        quiz_id=quiz_id,
        total_possible=len(quiz.questions) * 10
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    # Return questions (without correct answers)
    questions = []
    for q in quiz.questions:
        questions.append({
            "id": q.id,
            "question_number": q.question_number,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": json.loads(q.options) if q.options else None,
            "color_hint": q.color_hint,
            "points": q.points
        })
    
    return {
        "attempt_id": attempt.id,
        "quiz_title": quiz.title,
        "questions": questions,
        "total_questions": len(questions)
    }


@router.post("/submit", response_model=QuizResultResponse)
def submit_quiz(
    submission: QuizSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit quiz answers and get results."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can submit quizzes")
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Get attempt
    attempt = db.query(QuizAttempt).filter(QuizAttempt.id == submission.quiz_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")
    
    if attempt.student_id != student.id:
        raise HTTPException(status_code=403, detail="Not your quiz attempt")
    
    # Get questions
    quiz = db.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
    questions = {q.id: q for q in quiz.questions}
    
    # Grade each answer
    score = 0
    feedback = []
    
    for question_id, answer in submission.answers.items():
        question = questions.get(int(question_id))
        if not question:
            continue
        
        is_correct = answer.strip().lower() == question.correct_answer.strip().lower()
        
        if is_correct:
            score += question.points
        
        # Record attempt
        question_attempt = QuestionAttempt(
            attempt_id=attempt.id,
            question_id=question.id,
            student_answer=answer,
            is_correct=is_correct
        )
        db.add(question_attempt)
        
        feedback.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "your_answer": answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "explanation": question.explanation
        })
    
    # Update attempt
    attempt.score = score
    attempt.passed = (score / attempt.total_possible * 100) >= quiz.passing_score
    attempt.completed_at = datetime.utcnow()
    
    # Award points
    points_earned = score
    student.total_points += points_earned
    
    # Record progress
    progress = ProgressRecord(
        user_id=current_user.id,
        record_type="quiz_complete",
        record_data=json.dumps({"quiz_id": quiz.id, "score": score}),
        points_earned=points_earned
    )
    db.add(progress)
    
    # Check for quiz badges
    quiz_count = len([a for a in student.quiz_attempts if a.passed])
    if attempt.passed and quiz_count == 1 and score == attempt.total_possible:
        check_and_award_badges(db, student, "quiz_perfect")
    
    db.commit()
    
    return QuizResultResponse(
        attempt_id=attempt.id,
        score=score,
        total_possible=attempt.total_possible,
        passed=attempt.passed,
        percentage=round(score / attempt.total_possible * 100, 1) if attempt.total_possible > 0 else 0,
        feedback=feedback
    )


@router.get("/attempts/history", response_model=List[dict])
def get_quiz_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get quiz attempt history for current student."""
    if current_user.role != "student":
        return []
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        return []
    
    attempts = []
    for attempt in student.quiz_attempts:
        quiz = attempt.quiz
        attempts.append({
            "id": attempt.id,
            "quiz_title": quiz.title,
            "score": attempt.score,
            "total_possible": attempt.total_possible,
            "passed": attempt.passed,
            "percentage": round(attempt.score / attempt.total_possible * 100, 1) if attempt.total_possible > 0 else 0,
            "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None
        })
    
    return attempts

"""Progress and dashboard router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models import (
    User, StudentProfile, ParentProfile, ProgressRecord,
    Badge, CompletedLesson, QuizAttempt
)
from backend.schemas import (
    DashboardResponse, BadgeResponse, ParentDashboardResponse, ParentStudentResponse
)
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get student dashboard data."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only for students")
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Get recent activity
    recent_records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id
    ).order_by(desc(ProgressRecord.created_at)).limit(10).all()
    
    recent_activity = []
    for record in recent_records:
        recent_activity.append({
            "type": record.record_type,
            "points": record.points_earned,
            "date": record.created_at.isoformat()
        })
    
    # Calculate weekly progress (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_records = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.created_at >= week_ago
    ).all()
    
    weekly_progress = {}
    for record in weekly_records:
        day = record.created_at.strftime("%a")
        if day not in weekly_progress:
            weekly_progress[day] = {"points": 0, "activities": 0}
        weekly_progress[day]["points"] += record.points_earned
        weekly_progress[day]["activities"] += 1
    
    # Count quizzes passed
    quizzes_passed = len([a for a in student.quiz_attempts if a.passed])
    
    return DashboardResponse(
        total_points=student.total_points,
        current_streak=student.current_streak,
        longest_streak=student.longest_streak,
        lessons_completed=len(student.completed_lessons),
        quizzes_passed=quizzes_passed,
        badges=[BadgeResponse.model_validate(b) for b in student.badges],
        recent_activity=recent_activity,
        weekly_progress=weekly_progress
    )


@router.get("/parent/dashboard", response_model=ParentDashboardResponse)
def get_parent_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get parent dashboard showing linked student's progress."""
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="Only for parents")
    
    parent = db.query(ParentProfile).filter(ParentProfile.user_id == current_user.id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    
    # Get all students (in a real app, this would be filtered by parent-student link)
    all_students = db.query(StudentProfile).all()
    
    student_responses = []
    for student in all_students:
        user = student.user
        quizzes_passed = len([a for a in student.quiz_attempts if a.passed])
        
        # Calculate study time
        total_study_time = sum(c.time_spent_minutes for c in student.completed_lessons)
        
        # Identify weak areas (lessons not completed, low quiz scores)
        weak_areas = []
        
        student_responses.append(ParentStudentResponse(
            student_id=student.id,
            student_name=user.full_name,
            total_points=student.total_points,
            current_streak=student.current_streak,
            longest_streak=student.longest_streak,
            lessons_completed=len(student.completed_lessons),
            quizzes_passed=quizzes_passed,
            recent_badges=[BadgeResponse.model_validate(b) for b in student.badges[-5:]],
            weak_areas=weak_areas,
            study_time_minutes=total_study_time
        ))
    
    # Find linked student
    linked = None
    if parent.linked_student_id:
        linked_student = next((s for s in student_responses if s.student_id == parent.linked_student_id), None)
        linked = linked_student
    
    return ParentDashboardResponse(
        linked_student=linked,
        all_students=student_responses
    )


@router.get("/badges", response_model=List[BadgeResponse])
def get_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all badges for current student."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only for students")
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        return []
    
    return [BadgeResponse.model_validate(b) for b in student.badges]


@router.get("/rap/progress", response_model=dict)
def get_rap_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get RAP card progress for student."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only for students")
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        return {"total": 0, "mastered": 0, "cards": []}
    
    return {
        "total": len(student.rap_cards),
        "mastered": len([c for c in student.rap_cards if c.is_mastered]),
        "cards": [
            {
                "card_id": c.rap_card_id,
                "times_practiced": c.times_practiced,
                "is_mastered": c.is_mastered
            }
            for c in student.rap_cards
        ]
    }

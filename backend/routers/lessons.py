"""Lessons router - content management and student progress."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import (
    User, Subject, Unit, Lesson, CompletedLesson, StudentProfile,
    Badge, ProgressRecord, RAPCard
)
from backend.schemas import (
    SubjectResponse, UnitResponse, LessonResponse,
    LessonCompleteRequest, LessonCompleteResponse, BadgeResponse
)
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/lessons", tags=["Lessons"])


def check_and_award_badges(db: Session, student: StudentProfile, trigger_type: str) -> Badge | None:
    """Check badge conditions and award if earned."""
    existing_badge_names = [b.badge_type for b in student.badges]
    
    new_badge = None
    
    # Streak badges
    if trigger_type == "streak" or trigger_type == "any":
        if student.current_streak == 3 and "streak_3" not in existing_badge_names:
            new_badge = Badge(
                student_id=student.id,
                badge_type="streak_3",
                badge_name="3-Day Streak! 🔥",
                description="Completed lessons 3 days in a row!",
                icon_emoji="🔥"
            )
        elif student.current_streak == 7 and "streak_7" not in existing_badge_names:
            new_badge = Badge(
                student_id=student.id,
                badge_type="streak_7",
                badge_name="Week Warrior! 💪",
                description="Completed lessons 7 days in a row!",
                icon_emoji="💪"
            )
        elif student.current_streak == 30 and "streak_30" not in existing_badge_names:
            new_badge = Badge(
                student_id=student.id,
                badge_type="streak_30",
                badge_name="Monthly Master! 🏆",
                description="Completed lessons 30 days in a row! Amazing!",
                icon_emoji="🏆"
            )
    
    # Lesson count badges
    lesson_count = len(student.completed_lessons)
    if trigger_type == "lesson" or trigger_type == "any":
        if lesson_count == 1 and "first_lesson" not in existing_badge_names:
            new_badge = Badge(
                student_id=student.id,
                badge_type="first_lesson",
                badge_name="First Step! 👣",
                description="Completed your first lesson!",
                icon_emoji="👣"
            )
        elif lesson_count == 10 and "lessons_10" not in existing_badge_names:
            new_badge = Badge(
                student_id=student.id,
                badge_type="lessons_10",
                badge_name="Getting Started! 🌟",
                description="Completed 10 lessons!",
                icon_emoji="🌟"
            )
        elif lesson_count == 50 and "lessons_50" not in existing_badge_names:
            new_badge = Badge(
                student_id=student.id,
                badge_type="lessons_50",
                badge_name="Halfway Hero! 🎯",
                description="Completed 50 lessons!",
                icon_emoji="🎯"
            )
    
    if new_badge:
        db.add(new_badge)
        student.total_points += 50
        db.commit()
        db.refresh(new_badge)
        return new_badge
    
    return None


@router.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    """Get all subjects with units and lessons."""
    subjects = db.query(Subject).all()
    return subjects


@router.get("/math", response_model=List[UnitResponse])
def get_math_units(db: Session = Depends(get_db)):
    """Get all Math units."""
    math = db.query(Subject).filter(Subject.name == "Math").first()
    if not math:
        return []
    return math.units


@router.get("/science", response_model=List[UnitResponse])
def get_science_units(db: Session = Depends(get_db)):
    """Get all Science units."""
    science = db.query(Subject).filter(Subject.name == "Science").first()
    if not science:
        return []
    return science.units


@router.get("/units/{unit_id}", response_model=UnitResponse)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    """Get a specific unit with all lessons."""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """Get a specific lesson with RAP cards."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/complete", response_model=LessonCompleteResponse)
def complete_lesson(
    request: LessonCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a lesson as completed and award points."""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can complete lessons")
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Check if already completed
    existing = db.query(CompletedLesson).filter(
        CompletedLesson.student_id == student.id,
        CompletedLesson.lesson_id == request.lesson_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Lesson already completed")
    
    # Mark as completed
    completed = CompletedLesson(
        student_id=student.id,
        lesson_id=request.lesson_id,
        time_spent_minutes=request.time_spent_minutes
    )
    db.add(completed)
    
    # Update streak
    today = datetime.utcnow().date()
    if student.last_activity_date:
        last_date = student.last_activity_date.date()
        if (today - last_date).days == 1:
            student.current_streak += 1
        elif (today - last_date).days > 1:
            student.current_streak = 1
    else:
        student.current_streak = 1
    
    student.last_activity_date = datetime.utcnow()
    
    if student.current_streak > student.longest_streak:
        student.longest_streak = student.current_streak
    
    # Award points
    points_earned = 10 + min(request.time_spent_minutes, 20)  # Base 10 + up to 20 bonus
    student.total_points += points_earned
    
    # Record progress
    progress = ProgressRecord(
        user_id=current_user.id,
        record_type="lesson_complete",
        record_data=str(request.lesson_id),
        points_earned=points_earned
    )
    db.add(progress)
    
    # Check for streak update
    if student.current_streak > 1:
        check_and_award_badges(db, student, "streak")
    
    # Check for lesson badges
    new_badge = check_and_award_badges(db, student, "lesson")
    
    db.commit()
    db.refresh(student)
    
    return LessonCompleteResponse(
        success=True,
        points_earned=points_earned,
        new_total_points=student.total_points,
        new_badge=BadgeResponse.model_validate(new_badge) if new_badge else None,
        new_streak=student.current_streak
    )


@router.get("/progress/completed", response_model=List[int])
def get_completed_lessons(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of completed lesson IDs for the current student."""
    if current_user.role != "student":
        return []
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        return []
    
    return [c.lesson_id for c in student.completed_lessons]

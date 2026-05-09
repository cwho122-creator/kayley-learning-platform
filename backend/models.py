"""SQLAlchemy models for the learning platform."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class UserRole(str, enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    ADMIN = "admin"


class UnitType(str, enum.Enum):
    MATH = "math"
    SCIENCE = "science"


# ─── User Models ────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    parent_profile = relationship("ParentProfile", back_populates="user", uselist=False)
    progress_records = relationship("ProgressRecord", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user")
    badges = relationship("Badge", back_populates="student")
    completed_lessons = relationship("CompletedLesson", back_populates="student")
    quiz_attempts = relationship("QuizAttempt", back_populates="student")
    rap_cards = relationship("RAPCardProgress", back_populates="student")
    chat_sessions = relationship("ChatSession", back_populates="student")


class ParentProfile(Base):
    __tablename__ = "parent_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    linked_student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=True)

    user = relationship("User", back_populates="parent_profile")
    chat_sessions = relationship("ChatSession", back_populates="parent")


# ─── Badge System ─────────────────────────────────────────────────────────────

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    badge_type = Column(String(100), nullable=False)
    badge_name = Column(String(255), nullable=False)
    description = Column(Text)
    icon_emoji = Column(String(10), default="🏆")
    earned_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="badges")


# ─── Lesson System ────────────────────────────────────────────────────────────

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # "Math" or "Science"
    color = Column(String(7), default="#6366F1")  # Hex color

    units = relationship("Unit", back_populates="subject")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    unit_number = Column(Integer, nullable=False)
    description = Column(Text)
    week_start = Column(Integer, nullable=False)
    week_end = Column(Integer, nullable=False)

    subject = relationship("Subject", back_populates="units")
    lessons = relationship("Lesson", back_populates="unit")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    title = Column(String(255), nullable=False)
    lesson_number = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, default=10)
    content = Column(Text, nullable=False)  # Markdown/HTML content
    has_movement_break = Column(Boolean, default=True)
    movement_break_after_minutes = Column(Integer, default=7)
    order_index = Column(Integer, default=0)

    unit = relationship("Unit", back_populates="lessons")
    quiz = relationship("Quiz", back_populates="lesson", uselist=False)
    rap_cards = relationship("RAPCard", back_populates="lesson")
    completed_by = relationship("CompletedLesson", back_populates="lesson")


class CompletedLesson(Base):
    __tablename__ = "completed_lessons"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    time_spent_minutes = Column(Integer, default=0)

    student = relationship("StudentProfile", back_populates="completed_lessons")
    lesson = relationship("Lesson", back_populates="completed_by")


# ─── RAP Strategy Cards ───────────────────────────────────────────────────────

class RAPCard(Base):
    __tablename__ = "rap_cards"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    card_number = Column(Integer, nullable=False)  # 1=Read, 2=Ask, 3=Put
    title = Column(String(255), nullable=False)
    description = Column(Text)
    example_text = Column(Text)
    checklist_items = Column(Text)  # JSON array stored as string

    lesson = relationship("Lesson", back_populates="rap_cards")
    student_progress = relationship("RAPCardProgress", back_populates="rap_card")


class RAPCardProgress(Base):
    __tablename__ = "rap_card_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    rap_card_id = Column(Integer, ForeignKey("rap_cards.id"), nullable=False)
    times_practiced = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, nullable=True)
    is_mastered = Column(Boolean, default=False)

    student = relationship("StudentProfile", back_populates="rap_cards")
    rap_card = relationship("RAPCard", back_populates="student_progress")


# ─── Quiz System ──────────────────────────────────────────────────────────────

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    max_questions = Column(Integer, default=5)
    passing_score = Column(Integer, default=70)

    lesson = relationship("Lesson", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="multiple_choice")  # multiple_choice, numeric, free_response
    options = Column(Text, nullable=True)  # JSON array for MC options
    correct_answer = Column(String(500), nullable=False)
    explanation = Column(Text)
    points = Column(Integer, default=10)
    color_hint = Column(String(50), nullable=True)  # Key word highlighting hint

    quiz = relationship("Quiz", back_populates="questions")
    attempts = relationship("QuestionAttempt", back_populates="question")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Integer, default=0)
    total_possible = Column(Integer, default=0)
    passed = Column(Boolean, default=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("StudentProfile", back_populates="quiz_attempts")
    quiz = relationship("Quiz")
    question_attempts = relationship("QuestionAttempt", back_populates="attempt")


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    student_answer = Column(String(500), nullable=True)
    is_correct = Column(Boolean, default=False)
    answered_at = Column(DateTime, default=datetime.utcnow)

    attempt = relationship("QuizAttempt", back_populates="question_attempts")
    question = relationship("QuizQuestion", back_populates="attempts")


# ─── Progress Tracking ────────────────────────────────────────────────────────

class ProgressRecord(Base):
    __tablename__ = "progress_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    record_type = Column(String(50), nullable=False)  # "lesson_complete", "quiz_pass", "badge_earned", "streak_update"
    record_data = Column(Text)  # JSON string with additional details
    points_earned = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_records")


# ─── AI Chat System ───────────────────────────────────────────────────────────

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("parent_profiles.id"), nullable=True)
    title = Column(String(255), default="New conversation")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="chat_sessions")
    parent = relationship("ParentProfile", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", order_by="ChatMessage.created_at")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "student" or "ai"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")

"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    PARENT = "parent"
    ADMIN = "admin"


# ─── Auth Schemas ─────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ─── Student Profile Schemas ──────────────────────────────────────────────────

class BadgeResponse(BaseModel):
    id: int
    badge_type: str
    badge_name: str
    description: Optional[str]
    icon_emoji: str
    earned_at: datetime

    class Config:
        from_attributes = True


class StudentProfileResponse(BaseModel):
    id: int
    total_points: int
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[datetime]
    badges: List[BadgeResponse] = []

    class Config:
        from_attributes = True


# ─── Lesson Schemas ───────────────────────────────────────────────────────────

class RAPCardResponse(BaseModel):
    id: int
    card_number: int
    title: str
    description: Optional[str]
    example_text: Optional[str]
    checklist_items: Optional[str]

    class Config:
        from_attributes = True


class LessonResponse(BaseModel):
    id: int
    title: str
    lesson_number: int
    duration_minutes: int
    content: str
    has_movement_break: bool
    movement_break_after_minutes: int
    rap_cards: List[RAPCardResponse] = []

    class Config:
        from_attributes = True


class UnitResponse(BaseModel):
    id: int
    title: str
    unit_number: int
    description: Optional[str]
    week_start: int
    week_end: int
    lessons: List[LessonResponse] = []

    class Config:
        from_attributes = True


class SubjectResponse(BaseModel):
    id: int
    name: str
    color: str
    units: List[UnitResponse] = []

    class Config:
        from_attributes = True


class LessonCompleteRequest(BaseModel):
    lesson_id: int
    time_spent_minutes: int


class LessonCompleteResponse(BaseModel):
    success: bool
    points_earned: int
    new_total_points: int
    new_badge: Optional[BadgeResponse] = None
    new_streak: int


# ─── Quiz Schemas ──────────────────────────────────────────────────────────────

class QuizQuestionResponse(BaseModel):
    id: int
    question_number: int
    question_text: str
    question_type: str
    options: Optional[str]
    color_hint: Optional[str]
    points: int

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    max_questions: int
    passing_score: int
    questions: List[QuizQuestionResponse] = []

    class Config:
        from_attributes = True


class QuizSubmissionRequest(BaseModel):
    quiz_id: int
    answers: dict[int, str]  # question_id -> answer


class QuizResultResponse(BaseModel):
    attempt_id: int
    score: int
    total_possible: int
    passed: bool
    percentage: float
    feedback: List[dict] = []


# ─── Progress Schemas ─────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    total_points: int
    current_streak: int
    longest_streak: int
    lessons_completed: int
    quizzes_passed: int
    badges: List[BadgeResponse]
    recent_activity: List[dict] = []
    weekly_progress: dict = {}


class ParentStudentResponse(BaseModel):
    student_id: int
    student_name: str
    total_points: int
    current_streak: int
    longest_streak: int
    lessons_completed: int
    quizzes_passed: int
    recent_badges: List[BadgeResponse]
    weak_areas: List[str] = []
    study_time_minutes: int


class ParentDashboardResponse(BaseModel):
    linked_student: Optional[ParentStudentResponse]
    all_students: List[ParentStudentResponse] = []


# ─── Chat Schemas ─────────────────────────────────────────────────────────────

class ChatMessageRequest(BaseModel):
    session_id: Optional[int] = None
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True


class ChatAskResponse(BaseModel):
    session_id: int
    message: ChatMessageResponse
    response: str  # AI's response text
    related_lesson: Optional[dict] = None  # {id, title} if matched


class ChatHistoryResponse(BaseModel):
    sessions: List[ChatSessionResponse]
    total_messages: int

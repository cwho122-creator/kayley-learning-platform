"""Router package."""
from backend.routers.auth import router as auth_router
from backend.routers.lessons import router as lessons_router
from backend.routers.quiz import router as quiz_router
from backend.routers.progress import router as progress_router
from backend.routers.ai_tutor import router as ai_router

__all__ = ["auth_router", "lessons_router", "quiz_router", "progress_router", "ai_router"]

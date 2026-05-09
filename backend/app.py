"""FastAPI main application - Kayley's ADHD-Friendly Learning Platform."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import init_db
from backend.routers import auth_router, lessons_router, quiz_router, progress_router
from backend.routers.ai_tutor import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    # Seed content is called inside init_db or separately
    from backend.main import seed_content
    seed_content()
    yield


app = FastAPI(
    title="Kayley's Learning Platform",
    description="ADHD-friendly learning platform for IB MYP Year 8",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(lessons_router)
app.include_router(quiz_router)
app.include_router(progress_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {"message": "Welcome to Kayley's Learning Platform! 🚀", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

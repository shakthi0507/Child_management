import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.base import Base
from app.database.session import engine
from app.api.goals import router as goal_router
from app.api.assessments import router as assessment_router
from app.api.summary import router as summary_router
from app.api.auth import router as auth_router
from app.api.children import router as child_router
from app.api.therapists import router as therapist_router
from app.api.assignments import router as assignment_router
from app.api.progress import router as progress_router
from app.api.voice_notes import router as voice_router
from app.api.recommendations import router as recommendation_router
from app.api.goal_milestones import router as goal_milestone_router
from app.api.assessment_sessions import router as assessment_session_router
from app.api.assessment_completion import router as assessment_completion_router
from app.api.goal_recommendations import router as goal_recommendation_router
from app.api.goal_review import router as goal_review_router
from app.api.goal_progress import router as goal_progress_router
from app.api.parent_dashboard import router as parent_dashboard_router
from app.api.assessment_result import router as assessment_result_router
from app.api.development_profile import router as development_profile_router
from app.api.therapist_media import router as therapist_media_router
from app.models import recommendation

from app.api.milestones import router as milestone_router
from app.models import milestone
from app.models import assessment_session
from app.models import development_profile
from app.models import goal_milestone
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Vaa API"
)

cors_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
if "*" in cors_origins:
    raise RuntimeError("CORS_ORIGINS must list exact trusted origins; '*' is not allowed.")
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["Accept-Ranges", "Content-Range", "Content-Length"],
    )



app.include_router(
    auth_router
)

app.include_router(
    therapist_media_router
)

app.include_router(
    development_profile_router
)

app.include_router(
    milestone_router
)

app.include_router(
    parent_dashboard_router
)

app.include_router(
    summary_router
)

app.include_router(
    goal_recommendation_router
)

app.include_router(
    goal_progress_router
)

app.include_router(
    assessment_result_router
)

app.include_router(
    child_router
)

app.include_router(
    assessment_session_router
) 

app.include_router(
    therapist_router
)

app.include_router(
    assessment_completion_router
)

app.include_router(
    goal_milestone_router
)

app.include_router(
    assignment_router
)

app.include_router(
    goal_router
)

app.include_router(
    goal_review_router
)

app.include_router(
    progress_router
)

app.include_router(
    assessment_router
)

app.include_router(
    voice_router
)

app.include_router(
    recommendation_router
)



@app.get("/")
def home():

    return {
        "message": "Vaa API running"
    }


@app.get("/health", include_in_schema=False)
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok"}

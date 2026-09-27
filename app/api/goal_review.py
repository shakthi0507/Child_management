from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import datetime


from app.database.deps import get_db

from app.models.goal_recommendation import GoalRecommendation

from app.models.goal import Goal

from app.core.dependencies import require_role



router = APIRouter(

    prefix="/goal-review",

    tags=["Goal Review"]

)

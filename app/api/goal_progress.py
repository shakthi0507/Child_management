from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import datetime


from app.database.deps import get_db

from app.models.goal_milestone import GoalMilestone

from app.services.progress_service import (
    calculate_goal_progress
)

from app.core.dependencies import (
    require_role,
    ensure_child_access
)
from app.models.goal import Goal



router = APIRouter(

    prefix="/goal-progress",

    tags=["Goal Progress"]

)



@router.put("/{milestone_id}")
def update_milestone(

    milestone_id:int,

    status:str,

    db:Session=Depends(get_db),

    therapist=Depends(
        require_role("THERAPIST")
    )

):


    milestone = (
        db.query(GoalMilestone)
        .filter(GoalMilestone.id == milestone_id)
        .first()
    )

    if not milestone:
        raise HTTPException(404, "Milestone not found")

    goal = db.query(Goal).filter(Goal.id == milestone.goal_id).first()
    if not goal:
        raise HTTPException(404, "Goal not found")
    ensure_child_access(goal.child_id, therapist, db, allow_admin=False)


    milestone.status=status


    if status=="COMPLETED":

        milestone.completed_date=datetime.utcnow()


    db.commit()


    progress = calculate_goal_progress(

        milestone.goal_id,

        db

    )


    return {

        "message":
        "Milestone updated",

        "progress":
        progress

    }
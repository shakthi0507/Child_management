from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db


from app.models.goal_milestone import GoalMilestone
from app.models.goal import Goal


from app.core.dependencies import (
    require_role,
    ensure_child_access
)

from app.schemas.goal_milestone import (
    GoalMilestoneCreate,
    GoalMilestoneResponse
)

router = APIRouter(

    prefix="/goal-milestones",

    tags=["Goal Milestones"]

)





# =====================================
# Therapist creates milestone
# =====================================

@router.post(
    "/",
    response_model=GoalMilestoneResponse)
def create_goal_milestone(

    data: GoalMilestoneCreate,

    db: Session = Depends(get_db),

    therapist=Depends(
        require_role(
            "THERAPIST"
        )
    )

):


    goal = (

        db.query(
            Goal
        )

        .filter(
            Goal.id ==
            data.goal_id
        )

        .first()

    )


    if not goal:

        raise HTTPException(
            404,
            "Goal not found"
        )

    ensure_child_access(goal.child_id, therapist, db, allow_admin=False)



    milestone = GoalMilestone(

        goal_id=data.goal_id,

        title=data.title
    )

    db.add(
        milestone
    )

    db.commit()

    db.refresh(
        milestone
    )


    return milestone


# =====================================
# Get milestones for goal
# =====================================

@router.get(
    "/goal/{goal_id}"
)
def get_goal_milestones(

    goal_id:int,

    db:Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN"))

):

    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(404, "Goal not found")
    ensure_child_access(goal.child_id, user, db)


    return (

        db.query(
            GoalMilestone
        )

        .filter(

            GoalMilestone.goal_id
            ==
            goal_id

        )

        .all()

    )








# =====================================
# Update milestone
# =====================================

@router.put(
    "/{milestone_id}"
)
def update_goal_milestone(

    milestone_id:int,

    data:dict,

    db:Session = Depends(get_db),

    therapist=Depends(
        require_role(
            "THERAPIST"
        )
    )

):


    milestone = (

        db.query(
            GoalMilestone
        )

        .filter(
            GoalMilestone.id ==
            milestone_id
        )

        .first()

    )


    if not milestone:

        raise HTTPException(
            404,
            "Milestone not found"
        )

    ensure_child_access(milestone.goal.child_id, therapist, db, allow_admin=False)



    if "title" in data:

        milestone.title = data["title"]



    if "status" in data:

        milestone.status = data["status"]



    db.commit()

    db.refresh(
        milestone
    )


    return milestone







# =====================================
# Delete milestone
# =====================================

@router.delete(
    "/{milestone_id}"
)
def delete_goal_milestone(

    milestone_id:int,

    db:Session = Depends(get_db),

    therapist=Depends(
        require_role(
            "THERAPIST"
        )
    )

):


    milestone = (

        db.query(
            GoalMilestone
        )

        .filter(
            GoalMilestone.id ==
            milestone_id
        )

        .first()

    )


    if not milestone:

        raise HTTPException(
            404,
            "Milestone not found"
        )

    ensure_child_access(milestone.goal.child_id, therapist, db, allow_admin=False)



    db.delete(
        milestone
    )

    db.commit()



    return {

        "message":
        "Milestone deleted successfully"

    }
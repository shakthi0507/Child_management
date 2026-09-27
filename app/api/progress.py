from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db


from app.models.progress import GoalProgress
from app.models.goal import Goal
from app.models.goal_milestone import GoalMilestone
from app.models.child import Child
from app.models.therapist_assignment import TherapistAssignment
from app.models.therapist import Therapist


from app.schemas.progress import (
    ProgressCreate,
    ProgressResponse
)


from app.core.dependencies import (
    require_role
)


router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


# ==========================================================
# HELPER
# ==========================================================

def get_goal(
    goal_id: int,
    db: Session
):

    goal = (

        db.query(Goal)

        .filter(
            Goal.id == goal_id
        )

        .first()

    )

    if not goal:

        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal


# ==========================================================
# CHECK PARENT ACCESS
# ==========================================================

def check_parent_goal_access(
    goal: Goal,
    user,
    db: Session
):

    child = (

        db.query(Child)

        .filter(
            Child.id == goal.child_id
        )

        .first()

    )

    if not child:

        raise HTTPException(
            status_code=404,
            detail="Child not found"
        )


    if child.parent_id != user["id"]:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


    return child


# ==========================================================
# CHECK THERAPIST ACCESS
# ==========================================================

def check_therapist_goal_access(
    goal: Goal,
    user,
    db: Session
):

    child = (

        db.query(Child)

        .filter(
            Child.id == goal.child_id
        )

        .first()

    )

    if not child:

        raise HTTPException(
            status_code=404,
            detail="Child not found"
        )


    therapist = (

        db.query(Therapist)

        .filter(
            Therapist.user_id == user["id"]
        )

        .first()

    )


    if not therapist:

        raise HTTPException(
            status_code=403,
            detail="Therapist profile not found"
        )


    assignment = (

        db.query(TherapistAssignment)

        .filter(

            TherapistAssignment.therapist_id
            == therapist.id,

            TherapistAssignment.child_id
            == child.id

        )

        .first()

    )


    if not assignment:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


    return child


# ==========================================================
# THERAPIST UPDATES MILESTONE PROGRESS
# ==========================================================

@router.post(
    "/",
    response_model=ProgressResponse
)
def create_progress(

    data: ProgressCreate,

    db: Session = Depends(get_db),

    therapist=Depends(
        require_role(
            "THERAPIST"
        )
    )

):


    # ------------------------------------------
    # Get goal
    # ------------------------------------------

    goal = get_goal(
        data.goal_id,
        db
    )


    # ------------------------------------------
    # Verify therapist has access to child
    # ------------------------------------------

    check_therapist_goal_access(
        goal,
        therapist,
        db
    )


    # ------------------------------------------
    # Get milestone
    # ------------------------------------------

    milestone = (

        db.query(
            GoalMilestone
        )

        .filter(
            GoalMilestone.id
            == data.milestone_id
        )

        .first()

    )


    if not milestone:

        raise HTTPException(
            status_code=404,
            detail="Milestone not found"
        )


    # ------------------------------------------
    # Make sure milestone belongs to goal
    # ------------------------------------------

    if milestone.goal_id != goal.id:

        raise HTTPException(

            status_code=400,

            detail=(
                "Milestone does not belong "
                "to this goal"
            )

        )


    # ------------------------------------------
    # Normalize status
    # ------------------------------------------

    status = data.status.upper()


    allowed_statuses = [
        "PENDING",
        "IN_PROGRESS",
        "COMPLETED"
    ]


    if status not in allowed_statuses:

        raise HTTPException(

            status_code=400,

            detail=(
                "Invalid status. Allowed values: "
                "PENDING, IN_PROGRESS, COMPLETED"
            )

        )


    # ------------------------------------------
    # Update milestone status
    # ------------------------------------------

    milestone.status = status


    # ------------------------------------------
    # Create progress history
    # ------------------------------------------

    progress = GoalProgress(

        goal_id=goal.id,

        milestone_id=milestone.id,

        updated_by=therapist["id"],

        status=status,

        notes=data.notes

    )


    db.add(progress)

    db.commit()

    db.refresh(progress)


    return progress


# ==========================================================
# VIEW GOAL PROGRESS HISTORY
# PARENT + THERAPIST
# ==========================================================

@router.get(
    "/goal/{goal_id}",
    response_model=list[ProgressResponse]
)
def get_progress(

    goal_id: int,

    db: Session = Depends(get_db),

    user=Depends(
        require_role(
            "PARENT",
            "THERAPIST",
            "ADMIN"
        )
    )

):


    # ------------------------------------------
    # Get goal
    # ------------------------------------------

    goal = get_goal(
        goal_id,
        db
    )


    # ------------------------------------------
    # Check access
    # ------------------------------------------

    if user["role"] == "PARENT":

        check_parent_goal_access(
            goal,
            user,
            db
        )


    elif user["role"] == "THERAPIST":

        check_therapist_goal_access(
            goal,
            user,
            db
        )


    # ------------------------------------------
    # Return progress history
    # ------------------------------------------

    return (

        db.query(
            GoalProgress
        )

        .filter(
            GoalProgress.goal_id
            == goal_id
        )

        .order_by(
            GoalProgress.id.desc()
        )

        .all()

    )


# ==========================================================
# CALCULATE GOAL PERCENTAGE
# PARENT + THERAPIST
# ==========================================================

@router.get(
    "/goal/{goal_id}/percentage"
)
def goal_percentage(

    goal_id: int,

    db: Session = Depends(get_db),

    user=Depends(
        require_role(
            "PARENT",
            "THERAPIST"
        )
    )

):


    # ------------------------------------------
    # Get goal
    # ------------------------------------------

    goal = get_goal(
        goal_id,
        db
    )


    # ------------------------------------------
    # Check access
    # ------------------------------------------

    if user["role"] == "PARENT":

        check_parent_goal_access(
            goal,
            user,
            db
        )


    elif user["role"] == "THERAPIST":

        check_therapist_goal_access(
            goal,
            user,
            db
        )


    # ------------------------------------------
    # Get milestones
    # ------------------------------------------

    milestones = (

        db.query(
            GoalMilestone
        )

        .filter(
            GoalMilestone.goal_id
            == goal_id
        )

        .all()

    )


    # ------------------------------------------
    # No milestones
    # ------------------------------------------

    if not milestones:

        return {

            "goal_id":
                goal_id,

            "total_milestones":
                0,

            "completed_milestones":
                0,

            "percentage":
                0

        }


    # ------------------------------------------
    # Count completed milestones
    # ------------------------------------------

    completed = len(

        [

            milestone

            for milestone in milestones

            if milestone.status
            and milestone.status.upper()
            == "COMPLETED"

        ]

    )


    percentage = (

        completed /

        len(milestones)

    ) * 100


    return {

        "goal_id":
            goal_id,

        "total_milestones":
            len(milestones),

        "completed_milestones":
            completed,

        "percentage":
            round(
                percentage,
                2
            )

    }
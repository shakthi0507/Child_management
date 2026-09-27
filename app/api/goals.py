from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.goal import Goal

from app.schemas.goal import (
    GoalCreate,
    GoalUpdate,
    GoalResponse
)

from app.core.dependencies import (
    require_role,
    ensure_child_access
)



router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)





# Therapist creates goal

@router.post(
    "/",
    response_model=GoalResponse
)
def create_goal(

    data: GoalCreate,

    db: Session = Depends(get_db),

    therapist=Depends(
        require_role("THERAPIST")
    )

):

    ensure_child_access(data.child_id, therapist, db, allow_admin=False)


    goal = Goal(


        child_id=data.child_id,


        therapist_id=therapist["id"],


        assessment_session_id=
            data.assessment_session_id,


        domain=data.domain,


        current_level=data.current_level,


        short_term_goal=
            data.short_term_goal,


        long_term_goal=
            data.long_term_goal,


        duration_days=
            data.duration_days

    )


    db.add(goal)

    db.commit()

    db.refresh(goal)


    return goal






# Parent/Therapist view child goals

@router.get(
    "/child/{child_id}",
    response_model=list[GoalResponse]
)
def get_child_goals(

    child_id:int,

    db:Session=Depends(get_db),

    user=Depends(
    require_role(
        [
            "PARENT",
            "THERAPIST",
            "ADMIN"
        ]
    )
)

):

    ensure_child_access(child_id, user, db)


    return (

        db.query(Goal)

        .filter(
            Goal.child_id ==
            child_id
        )

        .all()

    )







# Therapist update goal

@router.put(
    "/{goal_id}",
    response_model=GoalResponse
)
def update_goal(

    goal_id:int,

    data:GoalUpdate,

    db:Session=Depends(get_db),

    therapist=Depends(
        require_role(
            "THERAPIST"
        )
    )

):


    goal = (

        db.query(Goal)

        .filter(
            Goal.id ==
            goal_id
        )

        .first()

    )


    if not goal:

        raise HTTPException(
            404,
            "Goal not found"
        )

    ensure_child_access(goal.child_id, therapist, db, allow_admin=False)



    goal.short_term_goal = (
        data.short_term_goal
    )


    goal.long_term_goal = (
        data.long_term_goal
    )


    goal.duration_days = (
        data.duration_days
    )


    goal.status = (
        data.status
    )


    db.commit()

    db.refresh(goal)


    return goal


@router.delete("/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    therapist=Depends(require_role("THERAPIST"))
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

    ensure_child_access(goal.child_id, therapist, db, allow_admin=False)


    db.delete(goal)
    db.commit()

    return {
        "message": "Goal deleted successfully"
    }


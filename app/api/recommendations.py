from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.goal import Goal
from app.models.goal_milestone import GoalMilestone
from app.models.development_profile import ChildDevelopmentProfile
from app.models.progress import GoalProgress

from app.services.recommendation_service import (
    generate_recommendations
)
from app.services.progress_service import calculate_goal_progress

from app.core.dependencies import (
    get_current_user,
    ensure_child_access
)



router = APIRouter(

    prefix="/recommendations",

    tags=["Recommendations"]

)





@router.get("/{child_id}")
def get_recommendations(

    child_id:int,

    db:Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )

):

    ensure_child_access(child_id, current_user, db)


    goals = (

        db.query(
            Goal
        )

        .filter(
            Goal.child_id ==
            child_id
        )

        .all()

    )



    profiles = db.query(ChildDevelopmentProfile).filter(
        ChildDevelopmentProfile.child_id == child_id
    ).all()
    domain_results = []
    for profile in profiles:
        score = profile.score_percentage or 0
        status = "ACHIEVED" if score >= 75 else "EMERGING" if score >= 40 else "DELAYED"
        domain_results.append({
            "domain": profile.domain,
            "current_level": profile.therapist_level or profile.system_level,
            "status": status,
        })

    goal_progress = []
    for goal in goals:
        progress = calculate_goal_progress(goal.id, db)
        if progress["total_milestones"] > 0:
            goal_progress.append(progress["percentage"])
    progress_percentage = (
        sum(goal_progress) / len(goal_progress)
        if goal_progress else None
    )



    recommendations = generate_recommendations(

        domain_results,

        goals,

        progress_percentage

    )



    return {


        "child_id":
            child_id,


        "active_goals":
            sum(1 for goal in goals if goal.status != "COMPLETED"),

        "progress_percentage": round(progress_percentage, 2) if progress_percentage is not None else None,


        "recommendations":
            recommendations

    }

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.development_profile import ChildDevelopmentProfile

from app.models.goal_recommendation import GoalRecommendation

from app.services.goal_recommendation_service import (
    generate_goal,
    calculate_priority
)


from app.core.dependencies import (
    require_role,
    ensure_child_access,
)



router = APIRouter(

    prefix="/goal-recommendations",

    tags=["Goal Recommendations"]

)


@router.post("/{child_id}")
def generate_recommendations(

    child_id:int,

    db:Session=Depends(get_db),

    therapist=Depends(
        require_role("THERAPIST")
    )

): 

    ensure_child_access(child_id, therapist, db, allow_admin=False)


    profiles = (

        db.query(
            ChildDevelopmentProfile
        )

        .filter(
            ChildDevelopmentProfile.child_id
            ==
            child_id
        )

        .all()

    )


    recommendations=[]



    for profile in profiles:


        priority = calculate_priority(

            profile.score_percentage

        )


        goals = generate_goal(

            profile.domain,

            profile.system_level

        )


        recommendation = GoalRecommendation(

            child_id=child_id,

            assessment_session_id=
            profile.assessment_session_id,

            domain=profile.domain,

            priority=priority,

            current_level=
            profile.system_level,

            development_gap=
            profile.development_gap,

            short_term_goal=
            goals["short"],

            long_term_goal=
            goals["long"],

            duration_days=90

        )


        db.add(
            recommendation
        )


        recommendations.append(
            recommendation
        )


    db.commit()



    return {

        "message":
        "Recommendations generated",

        "count":
        len(recommendations)

    }

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db


from app.models.child import Child
from app.models.goal import Goal
from app.models.goal_milestone import GoalMilestone
from app.models.development_profile import ChildDevelopmentProfile


from app.services.progress_service import (
    calculate_goal_progress
)


from app.core.dependencies import (
    require_role,
    ensure_child_access
)



router = APIRouter(

    prefix="/parent-dashboard",

    tags=["Parent Dashboard"]

)





@router.get("/{child_id}")
def parent_dashboard(

    child_id:int,

    db:Session=Depends(get_db),

    parent=Depends(
        require_role("PARENT")
    )

):

    ensure_child_access(child_id, parent, db)


    child = (

        db.query(
            Child
        )

        .filter(
            Child.id ==
            child_id
        )

        .first()

    )


    if not child:

        raise HTTPException(
            404,
            "Child not found"
        )



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



    goals = (

        db.query(
            Goal
        )

        .filter(
            Goal.child_id
            ==
            child_id
        )

        .all()

    )



    goal_data=[]



    for goal in goals:


        progress = calculate_goal_progress(

            goal.id,

            db

        )


        milestones=(

            db.query(
                GoalMilestone
            )

            .filter(
                GoalMilestone.goal_id
                ==
                goal.id
            )

            .all()

        )


        goal_data.append({

            "domain":
            goal.domain,


            "short_term_goal":
            goal.short_term_goal,


            "long_term_goal":
            goal.long_term_goal,


            "duration_days":
            goal.duration_days,


            "progress":
            progress,


            "milestones":[

                {

                "title":m.title,

                "status":m.status

                }

                for m in milestones

            ]

        })





    return {


        "child":{

            "id":child.id,

            "name":child.name,

            "dob":child.dob

        },


        "development_profile":[


            {

            "domain":p.domain,

            "level":p.system_level,

            "gap":p.development_gap


            }

            for p in profiles


        ],



        "goals":goal_data

    }
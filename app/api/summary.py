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
from app.models.progress import GoalProgress

from app.models.development_profile import (
    ChildDevelopmentProfile
)


from app.core.dependencies import (
    get_current_user,
    ensure_child_access
)



router = APIRouter(

    prefix="/children",

    tags=["Summary"]

)







@router.get("/{child_id}/summary")
def child_summary(


    child_id: int,


    db: Session = Depends(get_db),


    current_user = Depends(
        get_current_user
    )


):

    ensure_child_access(child_id, current_user, db)


    # =========================
    # Child
    # =========================


    child = (

        db.query(
            Child
        )

        .filter(
            Child.id == child_id
        )

        .first()

    )


    if not child:

        raise HTTPException(

            status_code=404,

            detail="Child not found"

        )






    # =========================
    # Development Profile
    # =========================


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




    domains = []



    for profile in profiles:


        domains.append({

            "domain":
                profile.domain,


            "development_level":
                profile.system_level,


            "therapist_level":
                profile.therapist_level,


            "confirmed":
                profile.confirmed

        })








    # =========================
    # Goals Summary
    # =========================


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




    goal_summary = []




    for goal in goals:



        # Get milestones count

        milestones = (

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



        total_milestones = len(
            milestones
        )




        # Get progress records

        progress_records = (

            db.query(
                GoalProgress
            )

            .filter(

                GoalProgress.goal_id
                ==
                goal.id

            )

            .all()

        )





        completed = len(
            [
                milestone for milestone in milestones
                if milestone.status
                and milestone.status.upper() == "COMPLETED"
            ]
        )





        total_progress = len(
            progress_records
        )




        percentage = 0



        if total_milestones > 0:


            percentage = (

                completed /

                total_milestones

            ) * 100





        goal_summary.append({

            "goal_id":
                goal.id,


            "domain":
                goal.domain,


            "short_term_goal":
                goal.short_term_goal,


            "long_term_goal":
                goal.long_term_goal,


            "total_milestones":
                total_milestones,


            "total_progress_records":
                total_progress,


            "completed_progress_records":
                completed,


            "progress":
                round(
                    percentage,
                    2
                )

        })









    # =========================
    # Parent Friendly Summary
    # =========================


    message = (

        f"{child.name} development summary "
        "is generated based on assessment "
        "results and therapy progress."

    )







    return {



        "child": {


            "id":
                child.id,


            "name":
                child.name,


            "gender":
                child.gender,


            "dob":
                child.dob

        },



        "development_domains":

            domains,



        "goals":

            goal_summary,



        "summary":

            message

    }
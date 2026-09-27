from sqlalchemy.orm import Session

from app.models.goal_milestone import GoalMilestone



def calculate_goal_progress(

    goal_id:int,

    db:Session

):


    milestones = (

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


    total = len(milestones)


    if total == 0:

        return {

            "total_milestones":0,

            "completed":0,

            "percentage":0

        }



    completed = len([

        m for m in milestones

        if m.status == "COMPLETED"

    ])



    percentage = (

        completed / total

    ) * 100



    return {

        "total_milestones":total,

        "completed":completed,

        "percentage":round(
            percentage,
            2
        )

    }
from sqlalchemy.orm import Session


from app.models.assessment_response import AssessmentResponse
from app.models.assessment_question import AssessmentQuestion
from app.models.milestone import Milestone
from app.models.child import Child
from app.models.development_profile import (
    ChildDevelopmentProfile
)




def generate_development_profile(

    session_id:int,

    child_id:int,

    db:Session

):


    responses = (

        db.query(
            AssessmentResponse
        )

        .filter(

            AssessmentResponse.session_id
            ==
            session_id

        )

        .all()

    )



    domain_scores = {}



    for response in responses:


        question = (

            db.query(
                AssessmentQuestion
            )

            .filter(

                AssessmentQuestion.id
                ==
                response.question_id

            )

            .first()

        )


        if not question:

            continue



        milestone = (

            db.query(
                Milestone
            )

            .filter(

                Milestone.id
                ==
                question.milestone_id

            )

            .first()

        )


        if not milestone:

            continue




        domain = milestone.domain



        if domain not in domain_scores:

            domain_scores[domain] = []



        domain_scores[domain].append({

            "milestone":
                milestone,


            "score":
                response.score

        })







    profiles = []





    for domain, items in domain_scores.items():

        scored = [item["score"] for item in items if item["score"] is not None]
        if not scored:
            continue
        score_percentage = round((sum(scored) / (2 * len(scored))) * 100)



        achieved = []


        for item in items:


            if item["score"] == 2:

                achieved.append(
                    item["milestone"]
                )





        # Highest achieved milestone

        if achieved:


            highest = max(

                achieved,

                key=lambda x:
                    x.expected_month

            )


            level = (

                f"{highest.expected_month}"
                " months"

            )



        else:


            level = "Below expected level"







        profile = ChildDevelopmentProfile(

            child_id=child_id,

            assessment_session_id=session_id,

            domain=domain,

            system_level=level,

            therapist_level=None,

            confirmed=False,
            score_percentage=score_percentage

        )


        db.add(
            profile
        )


        profiles.append(
            profile
        )



    db.commit()



    return profiles

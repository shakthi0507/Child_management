from sqlalchemy.orm import Session

from app.models.assessment_response import AssessmentResponse
from app.models.assessment_question import AssessmentQuestion
from app.models.milestone import Milestone



SCORES = {

    "ACHIEVED": 2,

    "EMERGING": 1,

    "DELAYED": 0,

    "NOT_APPLICABLE": None

}



def get_score(answer:str):

    return SCORES.get(
        answer.upper(),
        0
    )





def calculate_domain_results(

    session_id:int,

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



    domain_results = {}



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



        score = get_score(
            response.answer
        )



        if score is None:

            continue



        domain = milestone.domain



        if domain not in domain_results:

            domain_results[domain] = {

                "total_score":0,

                "max_score":0,

                "questions":0

            }



        domain_results[domain][
            "total_score"
        ] += score



        domain_results[domain][
            "max_score"
        ] += 2



        domain_results[domain][
            "questions"
        ] += 1





    results=[]



    for domain,data in domain_results.items():


        percentage = (

            data["total_score"]

            /

            data["max_score"]

        ) * 100



        results.append({

            "domain":domain,

            "score":
                data["total_score"],

            "percentage":
                round(
                    percentage,
                    2
                )

        })



    return results

def calculate_development_level(

    child_age_months:int,

    domain:str,

    responses,

    db

):


    achieved_milestones = []


    for response in responses:


        question = (

            db.query(
                AssessmentQuestion
            )

            .filter(
                AssessmentQuestion.id ==
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
                Milestone.id ==
                question.milestone_id
            )

            .first()

        )


        if not milestone:
            continue



        if (
            milestone.domain == domain
            and
            response.answer.upper()
            ==
            "ACHIEVED"
        ):

            achieved_milestones.append(
                milestone.age_group
            )


    if not achieved_milestones:

        return "Below baseline"


    return max(
        achieved_milestones
    )
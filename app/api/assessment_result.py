from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.assessment_session import AssessmentSession
from app.models.assessment_response import AssessmentResponse
from app.models.assessment_question import AssessmentQuestion

from app.services.assessment_scoring import calculate_score, calculate_percentage
from app.core.dependencies import require_role, ensure_child_access


router = APIRouter(
    prefix="/assessment-result",
    tags=["Assessment Result"]
)


@router.get("/{session_id}")
def get_assessment_result(

    session_id:int,

    child_id: int | None = None,

    db:Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN"))

):

    session = (
        db.query(AssessmentSession)
        .filter(
            AssessmentSession.id == session_id
        )
        .first()
    )


    if not session:

        raise HTTPException(
            404,
            "Assessment session not found"
        )

    if child_id is not None and session.child_id != child_id:
        raise HTTPException(400, "Child does not belong to this assessment session")

    ensure_child_access(session.child_id, user, db)


    responses = (

        db.query(
            AssessmentResponse
        )

        .filter(
            AssessmentResponse.session_id == session_id
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
                AssessmentQuestion.id ==
                response.question_id
            )

            .first()

        )


        if not question:
            continue


        score = calculate_score(
            response.answer
        )


        domain = question.milestone.domain


        if domain not in domain_scores:

            domain_scores[domain] = []


        if score is not None:

            domain_scores[domain].append(score)



    result=[]


    for domain, scores in domain_scores.items():

        total=sum(scores)

        max_score=len(scores)*2

        percentage=(total/max_score)*100 if max_score else 0


        if not scores:
            status="NOT_SCORED"

        elif percentage >= 75:

            status="ACHIEVED"

        elif percentage >=40:

            status="EMERGING"

        else:

            status="DELAYED"



        result.append({

            "domain":domain,

            "score":total,

            "percentage":round(
                percentage,
                2
            ),

            "status":status

        })


    all_scores = [score for scores in domain_scores.values() for score in scores]
    total = len(all_scores) * 2
    overall_percentage = calculate_percentage(all_scores)

    return {

        "child_id":session.child_id,

        "session_id":session.id,

        "percentage": overall_percentage,

        "status":session.status,

        "domains":result

    }

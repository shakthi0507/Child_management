from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db


from app.models.assessment_session import AssessmentSession

from app.models.development_profile import ChildDevelopmentProfile

from app.services.assessment_engine import (
    calculate_domain_results
)


from app.core.dependencies import (
    require_role
)



router = APIRouter(

    prefix="/assessment-completion",

    tags=["Assessment Completion"]

)





@router.post("/{session_id}/complete")
def complete_assessment(

    session_id:int,

    db:Session = Depends(get_db),

    therapist=Depends(
        require_role("THERAPIST")
    )

):


    session = (

        db.query(
            AssessmentSession
        )

        .filter(
            AssessmentSession.id ==
            session_id
        )

        .first()

    )


    if not session:

        raise HTTPException(
            404,
            "Assessment session not found"
        )



    results = calculate_domain_results(

        session_id,

        db

    )



    profiles = []



    for item in results:


        profile = ChildDevelopmentProfile(

            child_id=session.child_id,

            assessment_session_id=session.id,

            domain=item["domain"],

            system_level="Calculated",

            score_percentage=item["percentage"],

            development_gap="To calculate",

            confirmed=False

        )


        db.add(profile)

        profiles.append(profile)



    session.status="COMPLETED"


    db.commit()



    return {

        "message":
        "Assessment completed",

        "domains":
        results

    }
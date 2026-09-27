from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.deps import get_db

from app.models.assessment_session import AssessmentSession
from app.core.dependencies import require_role, ensure_child_access
from app.models.development_profile import ChildDevelopmentProfile

from app.models.assessment_response import AssessmentResponse

from app.models.assessment_question import AssessmentQuestion

from app.services.assessment_scoring import calculate_score



router = APIRouter(
    prefix="/development-profile",
    tags=["Development Profile"]
)


class DevelopmentProfileConfirm(BaseModel):
    therapist_level: str | None = None
    clinical_interpretation: str | None = None
    confirmed: bool = True

@router.put("/{profile_id}/confirm")
def confirm_profile(

    profile_id: int,

    data: DevelopmentProfileConfirm,

    db: Session = Depends(get_db),

    therapist=Depends(
        require_role("THERAPIST")
    )

):

    profile = (

        db.query(
            ChildDevelopmentProfile
        )

        .filter(
            ChildDevelopmentProfile.id == profile_id
        )

        .first()

    )


    if not profile:

        raise HTTPException(
            404,
            "Development profile not found"
        )

    ensure_child_access(profile.child_id, therapist, db, allow_admin=False)


    if data.therapist_level is not None:
        profile.therapist_level = data.therapist_level


    if data.clinical_interpretation is not None:
        profile.clinical_interpretation = data.clinical_interpretation


    profile.confirmed = data.confirmed


    db.commit()

    db.refresh(profile)


    return profile


@router.get("/session/{session_id}")
def get_session_profiles(
    session_id: int,
    child_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN")),
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(404, "Assessment session not found")
    if child_id is not None and session.child_id != child_id:
        raise HTTPException(400, "Child does not belong to this assessment session")
    ensure_child_access(session.child_id, user, db)
    return db.query(ChildDevelopmentProfile).filter(
        ChildDevelopmentProfile.assessment_session_id == session_id
    ).all()

@router.post("/generate/{session_id}")
def generate_profile(

    session_id:int,

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

    ensure_child_access(session.child_id, user, db)



    responses = (

        db.query(AssessmentResponse)

        .filter(
            AssessmentResponse.session_id == session_id
        )

        .all()

    )



    domain_scores = {}



    for response in responses:


        question = (

            db.query(AssessmentQuestion)

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




    profiles=[]



    for domain,scores in domain_scores.items():


        total = sum(scores)

        max_score = len(scores)*2


        percentage = (
            total/max_score if max_score else 0
        )*100



        if not scores:
            level="NOT_SCORED"

        elif percentage >=75:

            level="ACHIEVED"


        elif percentage >=40:

            level="EMERGING"


        else:

            level="DELAYED"



        profile = ChildDevelopmentProfile(

        child_id=session.child_id,

        assessment_session_id=session.id,

        domain=domain,

        system_level=level,

        score_percentage=round(percentage),

        confirmed=False

    )


        db.add(profile)

        profiles.append(profile)



    db.commit()



    return {

        "message":
        "Development profile generated",

        "profiles":[

            {
                "id": p.id,
                "domain":p.domain,
                "level":p.system_level
            }

            for p in profiles

        ]

    }

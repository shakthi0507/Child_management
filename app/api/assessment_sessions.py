from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.deps import get_db

from app.models.assessment_session import AssessmentSession

from app.models.assessment import Assessment

from app.models.child import Child

from app.core.dependencies import require_role, ensure_child_access
from app.schemas.assessment_session import (
    AssessmentSessionCreate,
    AssessmentSessionResponse
)


router = APIRouter(
    prefix="/assessment-sessions",
    tags=["Assessment Sessions"]
)

from fastapi import HTTPException


@router.put("/{session_id}")
def update_assessment_session(

    session_id: int,

    data: dict,

    db: Session = Depends(get_db),

    user=Depends(
        require_role("PARENT", "THERAPIST")
    )

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

    assessment = db.query(Assessment).filter(Assessment.id == session.assessment_id).first()
    expected_type = "PARENT_SCREENING" if user["role"] == "PARENT" else "THERAPIST_ASSESSMENT"
    if not assessment or assessment.assessment_type != expected_type:
        raise HTTPException(403, "Assessment session is not available for this role")
    if user["role"] == "THERAPIST" and session.therapist_id not in (None, user["id"]):
        raise HTTPException(403, "Assessment session belongs to another therapist")


    if "status" in data:
        session.status = data["status"]


    db.commit()

    db.refresh(session)


    return session

@router.post(
    "/",
    response_model=AssessmentSessionResponse
)
def create_session(

    data: AssessmentSessionCreate,

    db: Session = Depends(get_db),

    therapist=Depends(
        require_role("PARENT", "THERAPIST")
    )

):


    assessment = (

        db.query(Assessment)

        .filter(
            Assessment.id ==
            data.assessment_id
        )

        .first()

    )


    if not assessment:

        raise HTTPException(
            404,
            "Assessment not found"
        )

    if assessment.status != "PUBLISHED":
        raise HTTPException(404, "Published assessment not found")
    expected_type = "PARENT_SCREENING" if therapist["role"] == "PARENT" else "THERAPIST_ASSESSMENT"
    if assessment.assessment_type != expected_type:
        raise HTTPException(403, "Assessment is not available for this role")



    child = (

        db.query(Child)

        .filter(
            Child.id ==
            data.child_id
        )

        .first()

    )


    if not child:

        raise HTTPException(
            404,
            "Child not found"
        )

    ensure_child_access(child.id, therapist, db)



    session = AssessmentSession(

        assessment_id=data.assessment_id,

        child_id=data.child_id,

        therapist_id=therapist["id"] if therapist["role"] == "THERAPIST" else None,

        status="STARTED"

    )


    db.add(session)

    db.commit()

    db.refresh(session)


    return session





@router.get("/{child_id}")
def get_child_sessions(

    child_id:int,

    db:Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN"))

):

    ensure_child_access(child_id, user, db)


    return (

        db.query(AssessmentSession)

        .filter(
            AssessmentSession.child_id ==
            child_id
        )

        .all()

    )

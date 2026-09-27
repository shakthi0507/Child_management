from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db
from app.services.development_engine import (
    generate_development_profile
)

from app.models.assessment import Assessment
from app.models.milestone import Milestone
from app.models.assessment_question import AssessmentQuestion
from app.models.assessment_session import AssessmentSession
from app.models.assessment_response import AssessmentResponse
from app.models.development_profile import ChildDevelopmentProfile
from app.models.child import Child

from app.schemas.assessment import AssessmentCreate
from app.core.dependencies import get_current_user
from app.core.dependencies import (
    require_role,
    ensure_child_access
)


from app.services.assessment_scoring import calculate_score, calculate_percentage
from app.services.assessment_availability import age_group_applies, age_in_completed_months



router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"]
)



# ==========================
# CREATE ASSESSMENT
# ADMIN / THERAPIST
# ==========================


@router.post("/")
def create_assessment(

    data: AssessmentCreate,

    db: Session = Depends(get_db),

    current_user = Depends(require_role("ADMIN"))

):


    assessment = Assessment(

    name=data.name,

    description=data.description,

    assessment_type=data.assessment_type,

    age_group=data.age_group,

    domain=data.domain,

    created_by=current_user["id"]

)


    db.add(
        assessment
    )

    db.commit()

    db.refresh(
        assessment
    )


    return assessment





# ==========================
# GET ASSESSMENTS
# ==========================


@router.get("/")
def get_assessments(
    child_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Assessment).filter(Assessment.status == "PUBLISHED")
    if user["role"] == "PARENT":
        query = query.filter(Assessment.assessment_type == "PARENT_SCREENING")
    elif user["role"] == "THERAPIST":
        query = query.filter(Assessment.assessment_type == "THERAPIST_ASSESSMENT")
    assessments = query.all()
    if user["role"] == "PARENT" and child_id is not None:
        child = ensure_child_access(child_id, user, db)
        child_age_months = age_in_completed_months(child.dob)
        assessments = [
            assessment
            for assessment in assessments
            if age_group_applies(assessment.age_group, child_age_months)
        ]
    return assessments






# ==========================
# CREATE QUESTION
# ==========================


@router.post("/questions")
def create_question(

    data: dict,

    db: Session = Depends(get_db),

    user=Depends(
        require_role(
            "ADMIN"
        )
    )

):


    question = AssessmentQuestion(

        assessment_id=data[
            "assessment_id"
        ],

        milestone_id=data[
            "milestone_id"
        ],

        question=data[
            "question"
        ],

        order=data.get(
            "order",
            0
        )

    )


    db.add(
        question
    )

    db.commit()

    db.refresh(
        question
    )


    return question



# ==========================
# GET CHILD ASSESSMENTS
# ==========================


@router.get("/child/{child_id}")
def get_child_assessments(

    child_id:int,

    db:Session = Depends(get_db),

    current_user = Depends(
        get_current_user
    )

):

    ensure_child_access(child_id, current_user, db)


    query = db.query(Assessment).filter(Assessment.status == "PUBLISHED")
    if current_user["role"] == "PARENT":
        query = query.filter(Assessment.assessment_type == "PARENT_SCREENING")
    elif current_user["role"] == "THERAPIST":
        query = query.filter(Assessment.assessment_type == "THERAPIST_ASSESSMENT")
    assessments = query.all()

    if current_user["role"] == "PARENT":
        child = db.query(Child).filter(Child.id == child_id).first()
        child_age_months = age_in_completed_months(child.dob if child else None)
        assessments = [
            assessment
            for assessment in assessments
            if age_group_applies(assessment.age_group, child_age_months)
        ]


    return assessments

@router.get("/{assessment_id}/questions")
def get_questions(

    assessment_id:int,

    child_id: int | None = None,

    domain: str | None = None,

    db:Session=Depends(get_db),
    user=Depends(get_current_user)

):
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.status == "PUBLISHED",
    ).first()
    if not assessment:
        raise HTTPException(404, "Published assessment not found")
    if child_id is not None:
        ensure_child_access(child_id, user, db)
    allowed_type = {
        "PARENT": "PARENT_SCREENING",
        "THERAPIST": "THERAPIST_ASSESSMENT",
    }.get(user["role"])
    if allowed_type and assessment.assessment_type != allowed_type:
        raise HTTPException(403, "Assessment is not available for this role")
    question_query = db.query(AssessmentQuestion).filter(
        AssessmentQuestion.assessment_id == assessment_id
    )
    if domain is not None:
        question_query = question_query.join(AssessmentQuestion.milestone).filter(
            Milestone.domain == domain
        )
    questions = question_query.order_by(AssessmentQuestion.order).all()
    return [
        {
            "id": question.id,
            "assessment_id": question.assessment_id,
            "question": question.question,
            "order": question.order,
            "domain": question.milestone.domain,
        }
        for question in questions
    ]

# ==========================
# START ASSESSMENT SESSION
# ==========================


@router.post("/start")
def start_assessment(

    data: dict,

    db: Session = Depends(get_db),

    user=Depends(
        require_role(
            "PARENT",
            "THERAPIST"
        )
    )

):

    child_id = data["child_id"]
    ensure_child_access(child_id, user, db)

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == data["assessment_id"],
            Assessment.status == "PUBLISHED",
        )
        .first()
    )
    if not assessment:
        raise HTTPException(404, "Published assessment not found")
    if user["role"] == "PARENT" and assessment.assessment_type != "PARENT_SCREENING":
        raise HTTPException(403, "Parents can only start parent screening assessments")
    if user["role"] == "THERAPIST" and assessment.assessment_type != "THERAPIST_ASSESSMENT":
        raise HTTPException(403, "Therapists can only start therapist assessments")


    session = AssessmentSession(

        assessment_id=data[
            "assessment_id"
        ],

        child_id=data[
            "child_id"
        ],

        therapist_id=user["id"] if user["role"] == "THERAPIST" else None

    )


    db.add(
        session
    )

    db.commit()

    db.refresh(
        session
    )


    return session






# ==========================
# SUBMIT RESPONSE
# ==========================


@router.post("/responses")
def submit_response(

    data:dict,

    db:Session = Depends(get_db),

    user=Depends(
        require_role(
            "PARENT",
            "THERAPIST"
        )
    )

):

    session = (
        db.query(AssessmentSession)
        .filter(AssessmentSession.id == data.get("session_id"))
        .first()
    )
    if not session:
        raise HTTPException(404, "Assessment session not found")
    assessment = db.query(Assessment).filter(Assessment.id == session.assessment_id).first()
    expected_type = "PARENT_SCREENING" if user["role"] == "PARENT" else "THERAPIST_ASSESSMENT"
    if not assessment or assessment.assessment_type != expected_type:
        raise HTTPException(403, "Assessment is not available for this role")
    if user["role"] == "THERAPIST" and session.therapist_id not in (None, user["id"]):
        raise HTTPException(403, "Assessment session belongs to another therapist")
    ensure_child_access(session.child_id, user, db)

    question = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.id == data.get("question_id"))
        .first()
    )
    if not question or question.assessment_id != session.assessment_id:
        raise HTTPException(400, "Question does not belong to this assessment")


    score = calculate_score(
        data["answer"]
    )


    response = (
        db.query(AssessmentResponse)
        .filter(
            AssessmentResponse.session_id == session.id,
            AssessmentResponse.question_id == question.id,
        )
        .first()
    )
    if session.status == "COMPLETED":
        raise HTTPException(409, "Completed assessment responses cannot be changed")

    if response is None:
        response = AssessmentResponse(
            session_id=session.id,
            question_id=question.id,
        )
        db.add(response)

    response.answer = data["answer"]
    response.score = score
    response.therapist_remark = (
        data.get("therapist_remark") if user["role"] == "THERAPIST" else None
    )

    db.commit()

    db.refresh(
        response
    )


    return response


@router.post(
    "/{session_id}/complete"
)
def complete_assessment(
    session_id: int,
    child_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST")),
):
    session = (
        db.query(AssessmentSession)
        .filter(AssessmentSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(404, "Assessment session not found")
    if session.child_id != child_id:
        raise HTTPException(400, "Child does not belong to this assessment session")

    assessment = db.query(Assessment).filter(Assessment.id == session.assessment_id).first()
    expected_type = "PARENT_SCREENING" if user["role"] == "PARENT" else "THERAPIST_ASSESSMENT"
    if not assessment or assessment.assessment_type != expected_type:
        raise HTTPException(403, "Assessment is not available for this role")
    if user["role"] == "THERAPIST" and session.therapist_id not in (None, user["id"]):
        raise HTTPException(403, "Assessment session belongs to another therapist")

    ensure_child_access(child_id, user, db)
    if session.status == "COMPLETED":
        existing_profiles = db.query(ChildDevelopmentProfile).filter(
            ChildDevelopmentProfile.assessment_session_id == session_id
        ).count()
        return {
            "message": "Assessment completed successfully",
            "profiles_created": existing_profiles,
        }

    profiles = generate_development_profile(session_id, child_id, db)
    session.status = "COMPLETED"
    db.commit()

    return {
        "message": "Assessment completed successfully",
        "profiles_created": len(profiles),
    }


# ==========================
# RESULT
# ==========================


@router.get(
    "/{session_id}/result"
)
def assessment_result(
    session_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN")),
):
    session = (
        db.query(AssessmentSession)
        .filter(AssessmentSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(404, "Assessment session not found")
    ensure_child_access(session.child_id, user, db)

    responses = (
        db.query(AssessmentResponse)
        .filter(AssessmentResponse.session_id == session_id)
        .all()
    )
    scored = [item.score for item in responses if item.score is not None]
    percentage = calculate_percentage(scored)

    return {
        "session_id": session_id,
        "child_id": session.child_id,
        "percentage": percentage,
        "status": session.status,
    }


@router.get("/child/{child_id}/sessions")
def get_child_assessment_history(
    child_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN")),
):
    ensure_child_access(child_id, user, db)
    query = (
        db.query(AssessmentSession)
        .join(Assessment, Assessment.id == AssessmentSession.assessment_id)
        .filter(AssessmentSession.child_id == child_id)
    )
    if user["role"] == "PARENT":
        query = query.filter(Assessment.assessment_type == "PARENT_SCREENING")
    elif user["role"] == "THERAPIST":
        query = query.filter(
            Assessment.assessment_type.in_(["PARENT_SCREENING", "THERAPIST_ASSESSMENT"])
        )
    sessions = query.order_by(AssessmentSession.created_at.desc()).all()
    return [
        {
            "id": session.id,
            "child_id": session.child_id,
            "assessment_id": session.assessment_id,
            "assessment_name": session.assessment.name,
            "assessment_type": session.assessment.assessment_type,
            "status": session.status,
            "created_at": session.created_at,
        }
        for session in sessions
    ]


@router.get("/sessions/{session_id}/responses")
def get_assessment_session_responses(
    session_id: int,
    child_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("PARENT", "THERAPIST", "ADMIN")),
):
    session = db.query(AssessmentSession).filter(
        AssessmentSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(404, "Assessment session not found")
    if session.child_id != child_id:
        raise HTTPException(400, "Child does not belong to this assessment session")
    ensure_child_access(session.child_id, user, db)
    assessment = db.query(Assessment).filter(
        Assessment.id == session.assessment_id
    ).first()
    if user["role"] == "PARENT" and assessment.assessment_type != "PARENT_SCREENING":
        raise HTTPException(403, "Parents can only view parent screening assessments")
    if user["role"] == "THERAPIST" and assessment.assessment_type not in {
        "PARENT_SCREENING",
        "THERAPIST_ASSESSMENT",
    }:
        raise HTTPException(403, "Assessment is not available for this role")

    responses = db.query(AssessmentResponse).filter(
        AssessmentResponse.session_id == session_id
    ).all()
    return [
        {
            "id": response.id,
            "question_id": response.question_id,
            "question": response.question.question,
            "domain": response.question.milestone.domain,
            "answer": response.answer,
            "score": response.score,
            "therapist_remark": response.therapist_remark,
        }
        for response in responses
    ]

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.deps import get_db

from app.models.child import Child

from app.models.therapist import Therapist

from app.models.therapist_assignment import (
    TherapistAssignment
)

from app.schemas.assignment import (
    TherapistAssignmentCreate
)

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)

@router.post("/")
def assign_therapist(
    data: TherapistAssignmentCreate,
    db: Session = Depends(get_db)
):

    assignment = (
        TherapistAssignment(
            therapist_id=data.therapist_id,
            child_id=data.child_id
        )
    )

    db.add(assignment)

    db.commit()

    db.refresh(
        assignment
    )

    return assignment
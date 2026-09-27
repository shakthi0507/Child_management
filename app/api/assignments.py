from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.deps import get_db

from app.models.therapist_assignment import TherapistAssignment
from app.models.therapist import Therapist
from app.models.child import Child
from app.models.user import User

from app.schemas.assignment import AssignmentCreate

from app.core.dependencies import (
    require_role
)


router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)



# ADMIN assigns child to therapist
@router.post("/")
def assign_child(

    data: AssignmentCreate,

    db: Session = Depends(get_db),

    admin=Depends(
        require_role("ADMIN")
    )

):

    assignment = TherapistAssignment(

        therapist_id=data.therapist_id,

        child_id=data.child_id

    )


    db.add(assignment)

    db.commit()

    db.refresh(assignment)


    return assignment





# THERAPIST views assigned children
@router.get("/my-children")
def get_my_children(

    db: Session = Depends(get_db),

    therapist_user=Depends(
        require_role("THERAPIST")
    )

):

    therapist = (
        db.query(Therapist)
        .filter(
            Therapist.user_id ==
            therapist_user["id"]
        )
        .first()
    )


    if not therapist:

        raise HTTPException(
            status_code=404,
            detail="Therapist profile not found"
        )


    assignments = (
        db.query(TherapistAssignment)
        .filter(
            TherapistAssignment.therapist_id
            == therapist.id
        )
        .all()
    )


    children = []


    for item in assignments:

        child = (
            db.query(Child)
            .filter(
                Child.id ==
                item.child_id
            )
            .first()
        )


        if child:

            children.append(child)



    return children
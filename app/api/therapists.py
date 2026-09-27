from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.user import User

from app.models.therapist import Therapist

from app.schemas.therapist import TherapistCreate

from app.core.security import hash_password

from app.core.dependencies import require_role
from app.models.child import Child
from app.models.therapist import Therapist


router = APIRouter(
    prefix="/therapists",
    tags=["Therapists"]
)



@router.post("/")
def create_therapist(

    data: TherapistCreate,

    db: Session = Depends(get_db),

    admin=Depends(
        require_role("ADMIN")
    )

):


    existing = (
        db.query(User)
        .filter(
            User.email == data.email
        )
        .first()
    )


    if existing:

        raise HTTPException(
            400,
            "Email already exists"
        )


    user = User(

        username=data.username,

        email=data.email,

        password=hash_password(
            data.password
        ),

        role="THERAPIST"

    )


    db.add(user)

    db.flush()


    therapist = Therapist(

        user_id=user.id,

        specialization=data.specialization,

        experience=data.experience

    )


    db.add(therapist)

    db.commit()

    db.refresh(therapist)


    return therapist
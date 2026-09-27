from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError


from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)
from app.database.deps import get_db
from app.models.user import User
from app.models.child import Child
from app.models.therapist import Therapist
from app.models.therapist_assignment import TherapistAssignment
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )


        user_id = payload.get("id")
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is inactive or no longer exists"
            )

        return {
            "id": user.id,
            "sub": user.email,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }


    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )





def require_role(*required_roles):

    if len(required_roles) == 1 and isinstance(required_roles[0], (list, tuple, set)):
        required_roles = tuple(required_roles[0])


    def role_checker(

        current_user=Depends(
            get_current_user
        )

    ):


        user_role = current_user.get(
            "role"
        )



        if user_role not in required_roles:


            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Access denied"

            )



        return current_user



    return role_checker


def ensure_child_access(
    child_id: int,
    current_user: dict,
    db: Session,
    allow_admin: bool = True
) -> Child:
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")

    role = current_user.get("role")
    if allow_admin and role == "ADMIN":
        return child

    if role == "PARENT" and child.parent_id == current_user.get("id"):
        return child

    if role == "THERAPIST":
        assigned = (
            db.query(TherapistAssignment)
            .join(Therapist, Therapist.id == TherapistAssignment.therapist_id)
            .filter(
                Therapist.user_id == current_user.get("id"),
                TherapistAssignment.child_id == child_id
            )
            .first()
        )
        if assigned:
            return child

    raise HTTPException(status_code=403, detail="Access denied")
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.user import User

from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.core.dependencies import (
    get_current_user,
    require_role
)



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post(
    "/register",
    response_model=UserResponse
)
def register(

    user: UserRegister,

    db: Session = Depends(get_db)

):


    existing_user = (
        db.query(User)
        .filter(
            User.email == user.email
        )
        .first()
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )



    new_user = User(

        username=user.username,

        email=user.email,

        password=hash_password(
            user.password
        ),

        role="PARENT"

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user

@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin=Depends(require_role("ADMIN"))
):

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ]

@router.post("/login")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    db_user = (
        db.query(User)
        .filter(
            User.email == form_data.username
        )
        .first()
    )


    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    if not verify_password(
        form_data.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(

        {
            "sub": db_user.email,
            "id": db_user.id,
            "role": db_user.role
        }

    )


    return {

        "access_token": token,

        "token_type": "bearer"

    }



@router.get("/me")
def get_me(

    current_user = Depends(
        get_current_user
    )

):

    return current_user
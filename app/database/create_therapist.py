import os

from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password


db = SessionLocal()


existing = (
    db.query(User)
    .filter(
        (User.email == "therapist@test.com")
        | (User.username == "therapist1")
    )
    .first()
)

if existing:
    print("Therapist already exists", existing.id)
    db.close()
else:

    therapist_password = os.getenv("DEMO_THERAPIST_PASSWORD", "")
    if len(therapist_password) < 16:
        raise RuntimeError("Set DEMO_THERAPIST_PASSWORD to a value of at least 16 characters.")
    therapist = User(

        username="therapist1",

        email="therapist@test.com",

        password=hash_password(therapist_password),

        role="THERAPIST",

        is_active=True

    )

    db.add(therapist)

    db.commit()

    db.refresh(therapist)

    print(
        "Therapist created",
        therapist.id
    )

    db.close()

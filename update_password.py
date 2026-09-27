from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.user import User


db = SessionLocal()


new_password = "123456"


hashed_password = hash_password(new_password)


emails = [
    "stark@gmail.com",
    "shakthi@test.com",
    "admin@test.com"
]


for email in emails:

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user:

        user.password_hash = hashed_password

        print(
            f"Updated password for {email}"
        )

    else:

        print(
            f"User not found: {email}"
        )


db.commit()

db.close()


print("Password update completed")
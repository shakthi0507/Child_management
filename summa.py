from app.database.session import SessionLocal
from app.models.user import User

db = SessionLocal()

users = db.query(User).all()

for u in users:
    print(
        u.id,
        u.username,
        u.email,
        u.role
    )
    from app.core.security import verify_password

user = db.query(User).filter(
    User.email=="admin@test.com"
).first()

print(
    verify_password(
        "123456",
        user.password
    )
)
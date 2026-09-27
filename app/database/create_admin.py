import os

from app.database.session import SessionLocal

from app.models.user import User

from app.core.security import hash_password





db = SessionLocal()



existing_admin = (

    db.query(User)

    .filter(
        User.email ==
        "admin@test.com"
    )

    .first()

)



if existing_admin:


    print(
        "Admin already exists"
    )


else:

    admin_password = os.getenv("DEMO_ADMIN_PASSWORD", "")
    if len(admin_password) < 16:
        raise RuntimeError("Set DEMO_ADMIN_PASSWORD to a value of at least 16 characters.")


    admin = User(

        username="admin",

        email="admin@test.com",

        password=hash_password(admin_password),

        role="ADMIN",

        is_active=True

    )


    db.add(admin)

    db.commit()

    db.refresh(admin)



    print(
        "Admin created successfully"
    )


    print(
        "ID:",
        admin.id
    )



db.close()

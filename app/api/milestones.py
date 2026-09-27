from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from app.schemas.milestone import MilestoneCreate

from app.database.deps import get_db

from app.models.milestone import Milestone

from app.core.dependencies import (
    require_role
)



router = APIRouter(

    prefix="/milestones",

    tags=["Milestones"]

)





# ===================================
# Admin creates milestone
# ===================================

@router.post("/")
def create_milestone(

    data: MilestoneCreate,

    db: Session = Depends(get_db),

    admin=Depends(
        require_role(
            "ADMIN"
        )
    )

):


    milestone = Milestone(

    age_group=data.age_group,

    expected_month=data.expected_month,

    domain=data.domain,

    title=data.title,

    description=data.description

)


    db.add(
        milestone
    )

    db.commit()

    db.refresh(
        milestone
    )


    return milestone






# ===================================
# Get milestones
# Filter by domain / age
# ===================================

@router.get("/")
def get_milestones(

    domain:str | None = None,

    age_group:str | None = None,

    db:Session = Depends(get_db)

):


    query = db.query(
        Milestone
    )


    if domain:


        query = query.filter(

            Milestone.domain ==
            domain

        )



    if age_group:


        query = query.filter(

            Milestone.age_group ==
            age_group

        )



    return query.all()






# ===================================
# Get single milestone
# ===================================

@router.get("/{milestone_id}")
def get_milestone(

    milestone_id:int,

    db:Session = Depends(get_db)

):


    milestone = (

        db.query(
            Milestone
        )

        .filter(
            Milestone.id ==
            milestone_id
        )

        .first()

    )


    if not milestone:


        raise HTTPException(

            404,

            "Milestone not found"

        )


    return milestone






# ===================================
# Admin update milestone
# ===================================

@router.put("/{milestone_id}")
def update_milestone(

    milestone_id:int,

    data:dict,

    db:Session = Depends(get_db),

    admin=Depends(
        require_role(
            "ADMIN"
        )
    )

):


    milestone = (

        db.query(
            Milestone
        )

        .filter(
            Milestone.id ==
            milestone_id
        )

        .first()

    )


    if not milestone:


        raise HTTPException(

            404,

            "Milestone not found"

        )



    milestone.age_group = data[
        "age_group"
    ]


    milestone.expected_month = data[
        "expected_month"
    ]


    milestone.domain = data[
        "domain"
    ]


    milestone.title = data[
        "title"
    ]


    milestone.description = data.get(
        "description"
    )


    db.commit()

    db.refresh(
        milestone
    )


    return milestone






# ===================================
# Admin delete milestone
# ===================================

@router.delete("/{milestone_id}")
def delete_milestone(

    milestone_id:int,

    db:Session = Depends(get_db),

    admin=Depends(
        require_role(
            "ADMIN"
        )
    )

):


    milestone = (

        db.query(
            Milestone
        )

        .filter(
            Milestone.id ==
            milestone_id
        )

        .first()

    )


    if not milestone:


        raise HTTPException(

            404,

            "Milestone not found"

        )



    db.delete(
        milestone
    )

    db.commit()



    return {

        "message":
        "Milestone deleted successfully"

    }
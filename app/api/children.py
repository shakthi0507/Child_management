from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.deps import get_db

from app.models.child import Child

from app.models.user import User


from app.schemas.child import (
    ChildCreate,
    ChildResponse
)


from app.core.dependencies import (
    require_role
)



router = APIRouter(

    prefix="/children",

    tags=["Children"]

)





# ----------------------------------
# Create Child
# Parent only
# ----------------------------------

@router.post(
    "/",
    response_model=ChildResponse
)
def create_child(


    child: ChildCreate,


    current_user=Depends(

        require_role("PARENT")

    ),


    db: Session = Depends(get_db)

):


    parent = (

        db.query(User)

        .filter(

            User.email ==
            current_user["sub"]

        )

        .first()

    )



    if not parent:


        raise HTTPException(

            status_code=404,

            detail="Parent not found"

        )





    count = (

        db.query(Child)

        .count()

    ) + 1





    child_code = (

        f"CHD-{count:06d}"

    )





    new_child = Child(


        child_code=child_code,


        parent_id=parent.id,


        name=child.name,


        dob=child.dob,


        gender=child.gender,


        height=child.height,


        weight=child.weight

    )





    db.add(new_child)

    db.commit()

    db.refresh(new_child)




    return new_child







# ----------------------------------
# Get Parent Children
# Parent only
# ----------------------------------

@router.get(

    "/",

    response_model=list[ChildResponse]

)

def get_children(



    current_user=Depends(

        require_role("PARENT")

    ),



    db: Session = Depends(get_db)


):



    parent = (


        db.query(User)


        .filter(


            User.email ==

            current_user["sub"]


        )


        .first()


    )




    if not parent:


        raise HTTPException(

            status_code=404,

            detail="Parent not found"

        )






    return (

        db.query(Child)


        .filter(

            Child.parent_id ==

            parent.id

        )


        .all()

    )









# ----------------------------------
# Update Child
# Parent only
# ----------------------------------

@router.put(

    "/{child_id}",

    response_model=ChildResponse

)

def update_child(



    child_id:int,


    child_data:ChildCreate,



    current_user=Depends(

        require_role("PARENT")

    ),



    db:Session=Depends(get_db)


):



    parent = (

        db.query(User)


        .filter(

            User.email ==

            current_user["sub"]

        )


        .first()

    )





    child = (

        db.query(Child)


        .filter(


            Child.id == child_id,


            Child.parent_id == parent.id


        )


        .first()

    )





    if not child:



        raise HTTPException(

            status_code=404,

            detail="Child not found"

        )






    child.name = child_data.name

    child.dob = child_data.dob

    child.gender = child_data.gender

    child.height = child_data.height

    child.weight = child_data.weight






    db.commit()

    db.refresh(child)




    return child







# ----------------------------------
# Delete Child
# Parent only
# ----------------------------------

@router.delete(

    "/{child_id}"

)

def delete_child(



    child_id:int,



    current_user=Depends(

        require_role("PARENT")

    ),



    db:Session=Depends(get_db)


):



    parent = (


        db.query(User)


        .filter(


            User.email ==

            current_user["sub"]


        )


        .first()


    )





    child = (


        db.query(Child)


        .filter(


            Child.id == child_id,


            Child.parent_id == parent.id


        )


        .first()


    )





    if not child:



        raise HTTPException(

            status_code=404,

            detail="Child not found"

        )






    db.delete(child)

    db.commit()





    return {


        "message":

            "Child deleted successfully"

    }
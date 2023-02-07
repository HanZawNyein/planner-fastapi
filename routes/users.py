from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import Database

router = APIRouter(tags=['users'])

user_database = Database(User)


@router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    await user_database.save(user)
    return {"message": "User successfull registerd."}


@router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users does not exist."
        )
    if user_exist.password == user.password:
            return {"message": "User signed in Successfully."}
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Credentials Passed."
        )


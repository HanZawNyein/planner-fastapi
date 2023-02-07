from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

router = APIRouter(tags=['users'])

users = {}


@router.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    users[data.email] = data
    return {"message": "User successfull registerd."}

@router.post("/signin")
async def sign_user_in(user:UserSignIn)->dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users does not exist."
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong Credentials Passed."
        )
    
    return {"message":"User signed in Successfully."}
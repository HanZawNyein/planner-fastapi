from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, UserSignIn, TokenResponse
from database.connection import Database
from auth.hash_password import HashPassword
router = APIRouter(tags=['users'])

user_database = Database(User)
has_password = HashPassword()


@router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    hashed_password = has_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {"message": "User successfull registerd."}


@router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)

    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users does not exist."
        )
    if has_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong Credentials Passed."
    )

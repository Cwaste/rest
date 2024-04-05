from fastapi import APIRouter, HTTPException, status
from models import (User)
from schemas import (
    users as users_schema
)
from modules import (
    auth as auth_module
)
from pony.orm import db_session

router = APIRouter(
    prefix="/users",
   
    responses={404: {"description": "Not found"}},
)

@router.get("/sign_in")
async def login():
    return {"Hello": "World"}

@router.post("/sign_up")
@db_session
async def sign_up(user:users_schema.user_in):
    check_user = User.get(email=user.email)
    
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = User(
        firstName=user.firstName,
        middleName=user.middleName,
        lastName=user.lastName,
        careerID=user.careerID,
        rolID=user.rolID,
        email=user.email,
        password=auth_module.hash_password(user.password),
        avatar=user.avatar
    )
    
    return {"Hello": "World"}


from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from models import (Users)
from schemas import (
    users as users_schema
)
from modules import (
    auth as auth_module
)
from pony.orm import db_session, commit

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.post("/sign_in",status_code=status.HTTP_200_OK)
@db_session
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    check_user = Users.get(email=form_data.username)
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Users not found",
        )
    if not auth_module.hash_password(form_data.password) == check_user.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password",
        )
    user_id = int(check_user.ID)
    
    return {
        "access_token": auth_module.generate_token(user_id),
        "token_type": "bearer"
    }
    
@router.post("/sign_up",status_code=status.HTTP_201_CREATED)
@db_session
def sign_up(user: users_schema.user_in) :
    check_user = Users.get(email=user.email)
    
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = Users(
        first_Name = user.first_name,
        middle_Name = user.middle_name,
        last_name = user.last_name,
        country_ID = user.country_ID,
        email = user.email,
        phone = user.phone,
        password = auth_module.hash_password(user.password),
        avatar = user.avatar,
        rol_ID=2,
        created_at=datetime.datetime.today()
    )
    
    user.flush()
    user_id = int(user.ID)
    
    return   {
        "access_token": auth_module.generate_token(user_id),
        "token_type": "bearer"
    }

@router.get("/profile",status_code=status.HTTP_200_OK)
@db_session
def me(current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user = Users.get(ID=current_user)
    return user

@router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
@db_session
def delete_user(id:int,current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user_check = Users.get(ID=id)
    
    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = Users[id]
    user.delete()
    commit()
    return {"message":"User deleted"}

@router.put("/edit/{id}",status_code=status.HTTP_200_OK)
@db_session
def edit_user(id: int, user: users_schema.user_in, current_user: Annotated[str, Depends(auth_module.get_current_user_id)]):
    user_check = Users.get(ID=id)

    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    user_database = Users[id]
   
    user_database.set(
        firstName=user.firstName,
        middleName=user.middleName,
        lastName=user.lastName,
        careerID=user.careerID,
        rolID=user.rolID,
        email=user.email,
        password=auth_module.hash_password(user.password),
        avatar=user.avatar
        
    )
    
    commit()
   
    return {"message":"User updated"}
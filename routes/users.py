from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from models import (Users,Rols)
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
def sign_up(user: users_schema.user_in):
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
    
    if(user is None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return {"firstName":user.first_Name,
            "middleName":user.middle_Name,
            "lastName":user.last_name,
            "email":user.email,
            "rol":user.rol_ID.name,
            "points":user.points,
            "avatar":user.avatar}

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

@router.post("/create_user",status_code=status.HTTP_201_CREATED)
@db_session
def create_user(user: users_schema.user_in,rol:str):
    user_check = Users.get(email=user.email)
    
    if user_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    rol_id = 0
    if rol == "Usuario":
        rol_id = 2
    else:
        rol_id = 1
    
    user = Users(
        first_Name = user.first_name,
        middle_Name = user.middle_name,
        last_name = user.last_name,
        country_ID = user.country_ID,
        email = user.email,
        phone = user.phone,
        password = auth_module.hash_password(user.password),
        avatar = user.avatar,
        rol_ID=rol_id,
        created_at=datetime.datetime.today()
    )

    user.flush()
    return {"message":"User created"}
        
@router.get("/normal_users",status_code=status.HTTP_200_OK)
@db_session
def get_normal_users(search:str = None):
    data = []
    if search:
        users = Users.select(lambda user: user.rol_ID.name == "Usuario" and search in user.first_Name or search in user.middle_Name or search in user.last_name or search in user.email or search in user.phone)
    else:
        users = Users.select(lambda user: user.rol_ID.name == "Usuario")
    for user in users:
        data.append({
            "ID":user.ID,
            "firstName":user.first_Name,
            "middleName":user.middle_Name,
            "lastName":user.last_name,
            "email":user.email,
            "phone":user.phone,
            "avatar":user.avatar,
            "points":user.points
        })
    
    return data

@router.get("/administrator_users",status_code=status.HTTP_200_OK)
@db_session
def get_all_administrator_users(search:str = None):
    data = []
    if search:
        users = Users.select(lambda user: user.rol_ID.name == "Administrador" and search in user.first_Name or search in user.middle_Name or search in user.last_name or search in user.email or search in user.phone)
    else:
        users = Users.select(lambda user: user.rol_ID.name == "Administrador")
    
    
    for user in users:
        data.append({
            "ID":user.ID,
            "firstName":user.first_Name,
            "middleName":user.middle_Name,
            "lastName":user.last_name,
            "email":user.email,
            "phone":user.phone,
            "avatar":user.avatar,
            "points":user.points
        })
    
    return data

@router.delete("/{id}",status_code=status.HTTP_200_OK)
@db_session
def delete_user(id:int):
    user = Users.get(ID=id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    user.delete()
    return {"message":"User deleted"}
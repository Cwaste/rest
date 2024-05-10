from fastapi import APIRouter, HTTPException, status,Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from models import (Users,Countries)
from schemas import (
    users as users_schema
)
from modules import (
    auth as auth_module
)
from pony.orm import db_session, commit

router = APIRouter(
    prefix="/countries",
    responses={404: {"description": "Not found"}},
)

@router.get("/all",status_code=status.HTTP_200_OK)
@db_session
def get_countries():
    
    countries_data = []
    countries = Countries.select()
    
    for country in countries:
        countries_data.append(country.to_dict())
    
    return countries_data
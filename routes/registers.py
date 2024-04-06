from fastapi import APIRouter, HTTPException, status, Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import (Register)

from schemas import (registers as registers_schema)

from pony.orm import db_session, commit

router = APIRouter(
    prefix="/registers",
    responses={404: {"description": "Not found"}},
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
@db_session
def create_register(register: registers_schema.register_in):  
    
    #make corrects validations
    
    register = Register(
        name = register.name,
        userID = register.userID
    )
    

    return register

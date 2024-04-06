from fastapi import APIRouter, HTTPException, status, Depends
from typing import Any, List, Union
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import (Student)

from schemas import (students as students_schema)

from pony.orm import db_session, commit

router = APIRouter(
    prefix="/students",
    responses={404: {"description": "Not found"}},
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
@db_session
def create_register(students: students_schema.student_in):  
    
    #make corrects validations
    
    students = Student(
        firstName = students.firstName,
        middleName = students.middleName,
        lastName = students.lastName,
        carreerID = students.careerID,
        controlNumber = students.controlNumber,
    )
    

    return students
from pony.orm import *
from .base import db

class RegisterStudentRel(db.Entity):
    ID = PrimaryKey(int, auto = True)
    studentID = Required('Student')
    registerID = Required('Register')
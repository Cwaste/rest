from pony.orm import *
import time, datetime
from .base import db
from .registers_student_rel import RegisterStudentRel

class Register(db.Entity):
    ID = PrimaryKey(int, auto = True)
    name = Required(str)
    createdAt = Required(datetime.datetime, default = datetime.datetime.now)
    userID = Required('User')
    
    student = Set(lambda: RegisterStudentRel)
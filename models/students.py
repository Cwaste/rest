from pony.orm import *
import time, datetime
from .base import db
from .registers_student_rel import RegisterStudentRel

class Student(db.Entity):
    ID = PrimaryKey(int, auto = True)
    firstName = Required(str)
    middleName = Required(str)
    lastName = Required(str)
    carreerID = Required('Careers')
    controlNumber = Required(str)
    createdAt = Required(datetime.datetime, default = datetime.datetime.now)

    registers = Set(lambda: RegisterStudentRel)
from pony.orm import *
import time,datetime
from .base import db
from .students import Student

class Careers(db.Entity):
    ID = PrimaryKey(int, auto=True)
    name = Required(str)
    user = Set('User')

    students = Set(Student)

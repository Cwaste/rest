import os
from pony.orm import *
import time,datetime
from .base import db
from .rols import Rols
from .countries import Countries

class Users(db.Entity):
    ID = PrimaryKey(int, auto=True)
    first_Name = Required(str)
    middle_Name = Required(str)
    last_name = Required(str)
    country_ID =Required(Countries)
    email = Required(str)
    phone = Required(str)
    password = Required(str)
    avatar = Required(str)
    points = Required(int,default=0)
    rol_ID= Required(Rols,default=2)
    created_at = Required(datetime.date)
    
    achievement_ID = Set('User_achievement')
  
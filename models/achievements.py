import os
from pony.orm import *
import time,datetime
from .base import db



class Achievements(db.Entity):
    ID = PrimaryKey(int, auto=True)
    image = Required(str)
    points = Required(int)
    created_at = Required(datetime.date)
    
    achievement_user = Set('User_achievement')
    
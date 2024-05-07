import os
from pony.orm import *
import time,datetime
from .base import db
from .achievements import Achievements
from .users import Users

class User_achievement(db.Entity):
    ID = PrimaryKey(int, auto=True)
    user_ID = Required(Users)
    achievement_ID = Required(Achievements)
    
    
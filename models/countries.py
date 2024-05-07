import os
from pony.orm import *
import time,datetime
from .base import db
from .rols import Rols

class Countries(db.Entity):
    ID = PrimaryKey(int, auto=True)
    name = Required(str)
    
    user = Set('Users')
  
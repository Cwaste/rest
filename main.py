from models import db
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from routes import (
    users_router
)

load_dotenv()
db.bind(provider='mysql', host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), passwd=os.getenv('DB_PASSWORD'), db=os.getenv('DB_NAME'))
db.generate_mapping(create_tables=True)

app = FastAPI()
app.include_router(users_router)




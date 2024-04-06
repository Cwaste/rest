from pydantic import BaseModel

class register_in(BaseModel):
    name: str
    userID: int
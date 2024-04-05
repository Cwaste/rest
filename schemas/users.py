from pydantic import BaseModel,EmailStr
 
class user_in(BaseModel):
    firstName: str
    middleName: str
    lastName: str
    careerID: int
    rolID: int
    email: EmailStr
    password: str
    avatar: str
    
class user_out(BaseModel):
    id: int
    firstName: str
    middleName: str
    lastName: str
    careerID: int
    rolID: int
    email: EmailStr
    avatar: str
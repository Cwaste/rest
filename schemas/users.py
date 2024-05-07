from pydantic import BaseModel, EmailStr
 
class user_in(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    country_ID: int
    email: EmailStr
    phone: str
    password: str
    avatar: str
    
class user_out(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    country: str
    rol: str
    email: EmailStr
    phone: str
    password: str
    avatar: str

class sign_up_out(BaseModel):
    access_token: str
    token_type: str
    

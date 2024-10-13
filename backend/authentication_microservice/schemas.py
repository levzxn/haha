from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserIn(BaseModel):
    username:str
    email:str
    password:str

class UserOut(BaseModel):
    id:UUID
    username:str
    email:str
    created_at:datetime
    
    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    username:str
    password:str
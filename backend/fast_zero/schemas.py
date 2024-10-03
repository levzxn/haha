from pydantic import BaseModel
from datetime import datetime

class UserIn(BaseModel):
    username:str
    email:str
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    email:str
    created_at:datetime

class LoginSchema(BaseModel):
    username:str
    password:str

class DocumentOut(BaseModel):
    id: int
    file_name:str
    file_path:str
    sender:UserOut
    uploaded_at:datetime

class TokenData(BaseModel):
    username:str | None = None
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

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

class DocumentOut(BaseModel):
    id: UUID
    file_name:str
    file_path:str
    sender:UserOut
    uploaded_at:datetime

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username:str | None = None

class RefreshToken(BaseModel):
    refresh_token: str
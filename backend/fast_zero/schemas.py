from pydantic import BaseModel

class UserSchema(BaseModel):
    username:str
    email:str
    password:str

class LoginSchema(BaseModel):
    username:str
    password:str

class TokenData(BaseModel):
    username:str | None = None
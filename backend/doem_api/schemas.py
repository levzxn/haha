from pydantic import BaseModel,EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional


class EstabelecimentoOut(BaseModel):
    nome:str
    icone_path:Optional[str]
    pacote_id:UUID
    cidade:str

class UserIn(BaseModel):
    username:str
    email:str
    password:str

class UserOut(BaseModel):
    id:UUID
    username:str
    email:str
    created_at:datetime
    estabelecimento:EstabelecimentoOut
    
    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    username:str
    password:str

class DocumentOut(BaseModel):
    id: UUID
    file_name:str
    file_path:str
    sender:UUID
    uploaded_at:datetime

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username:str | None = None

class RefreshToken(BaseModel):
    refresh_token: str

class EmailIn(BaseModel):
    email_adress: EmailStr

class EmailOut(BaseModel):
    email:EmailStr
    subject:str
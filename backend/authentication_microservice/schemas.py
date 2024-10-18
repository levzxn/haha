from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import datetime
from typing import List,Optional


class LoginSchema(BaseModel):
    username:str
    password:str

class EstabelecimentoIn(BaseModel):
    nome:str
    pacote_id:UUID
    cidade:str

class EstabelecimentoOut(BaseModel):
    id:UUID
    nome:str
    icone_path:str
    pacote_id:UUID
    cidade:str

class UserIn(BaseModel):
    username:str
    email:str
    password:str
    is_admin:Optional[bool]=False
    estabelecimento:UUID

class UserOut(BaseModel):
    id:UUID
    username:str
    email:str
    created_at:datetime
    is_admin:bool
    estabelecimento:EstabelecimentoOut

class UptadedUser(BaseModel):
    username:Optional[str] = None
    email:Optional[str] = None
    password:Optional[str] = None
   

class TokenData(BaseModel):
    username:str | None = None    

class RefreshToken(BaseModel):
    refresh_token: str

class FuncionalidadeIn(BaseModel):
    nome:str

class FuncionalidadeOut(BaseModel):
    id:int
    nome:str

class PacoteIn(BaseModel):
    func_ids:List[int]

class PacoteOut(BaseModel):
    id:UUID
    created_at:datetime
    funcionalidades:List[FuncionalidadeOut]

class OrgaoIn(BaseModel):
    descricao:str
    cnpj:str
    endereco:str
    estabelecimento_id:UUID

class OrgaoOut(BaseModel):
    id:UUID
    descricao:str
    cnpj:str
    endereco:str
    estabelecimento:EstabelecimentoOut

class TokenResetIn(BaseModel):
    token_id:UUID

class EmailIn(BaseModel):
    email_adress: EmailStr

class EmailOut(BaseModel):
    email: EmailStr
    subject:str
    keys:dict
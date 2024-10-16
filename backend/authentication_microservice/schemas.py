from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class UserIn(BaseModel):
    username:str
    email:str
    password:str
    estabelecimento:UUID

    
    class Config:
        orm_mode = True

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

class UserOut(BaseModel):
    id:UUID
    username:str
    email:str
    created_at:datetime
    is_admin:bool
    estabelecimento:EstabelecimentoOut

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


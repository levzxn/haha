from pydantic import BaseModel

class ResponseUser(BaseModel):
    id:int
    username:str
    email:str

    class Config:
        orm_mode = True

class ResponseDoc(BaseModel):
    id:int
    file_name:str
    sender:ResponseUser

    class Config:
        orm_mode = True
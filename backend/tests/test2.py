from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id:Optional[int]=None
    name:Optional[str]=None
    email:Optional[str]=None

u1 = User(id=2,name='lucas')
print(u1)
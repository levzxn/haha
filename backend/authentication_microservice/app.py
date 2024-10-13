from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException,Depends
from authentication_microservice.routers import users
from authentication_microservice.schemas import UserIn,UserOut
from authentication_microservice.models import User
from authentication_microservice.security import get_password_hash,get_current_user
from http import HTTPStatus
from tortoise.expressions import Q
from typing import Annotated



app = FastAPI()

origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']

)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['authentication_microservice.models']},
    generate_schemas=True
)


T_User = Annotated[User,Depends(get_current_user)]


app.include_router(users.router)
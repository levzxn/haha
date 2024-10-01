from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fast_zero.routers import users,auth,docs
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']

)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(docs.router)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['fast_zero.models']},
    generate_schemas=True
)
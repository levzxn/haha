from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from doem_api.routers import docs,diario
from doem_api.middlewares import AuthMiddleware
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI, Request




app = FastAPI(docs_url="/documentation")
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']

)
app.add_middleware(AuthMiddleware)

app.include_router(docs.router)
app.include_router(diario.router)

register_tortoise(
    app,
    db_url="postgres://postgres:Lucasfr420@localhost:5432/DOEM",
    modules={'models': ['doem_api.models']},
    generate_schemas=True
)


@app.get('/')
async def root():
    return 'Rota Principal'
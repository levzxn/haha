from fastapi.routing import APIRouter
from fastapi import HTTPException,Depends
from authentication_microservice.schemas import FuncionalidadeIn,FuncionalidadeOut
from authentication_microservice.models import Funcionalidade
from http import HTTPStatus
from tortoise.exceptions import DoesNotExist

router = APIRouter(prefix='/func',tags=['funcionalidades'])

@router.post('/',response_model=FuncionalidadeOut)
async def create_func(func=FuncionalidadeIn):
    try:
        func = await Funcionalidade.create(nome=func.nome)
        return func
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro ao criar funcionalidade: {e}'
        )


@router.get('/{id}',response_model=FuncionalidadeOut)
async def get_func(id:int):
    try:
        func = await Funcionalidade.get(id=id)
        return func
    except DoesNotExist:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            detail='Id de Funcionalidade não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro de servidor: {e}'
        )
    
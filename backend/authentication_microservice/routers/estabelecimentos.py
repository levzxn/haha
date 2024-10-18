from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Request
from authentication_microservice.models import Estabelecimento,Pacote
from authentication_microservice.schemas import EstabelecimentoIn,EstabelecimentoOut
from http import HTTPStatus
from tortoise.expressions import Q
from tortoise.exceptions import DoesNotExist
from typing import Annotated


router = APIRouter(prefix='/estabelecimento',tags=['estabelecimento'])

@router.post('/',response_model=EstabelecimentoOut)
async def criar_estabelecimento(request:Request,estabelecimento:EstabelecimentoIn):
    connection = request.state.connection
    try:
        pacote = await Pacote.get(id=estabelecimento.pacote_id)
        estabelecimento_criado = await Estabelecimento.create(nome=estabelecimento.nome,icone_path="foto.png",pacote=pacote,cidade=estabelecimento.cidade,using_db=connection)
        return estabelecimento_criado
    except DoesNotExist:
        await connection.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Não foi possível criar Estabelecimento, Id do pacote não existe'
        )

#@router.get('/{id}')
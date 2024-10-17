from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from authentication_microservice.models import Estabelecimento,Pacote,Funcionalidade
from authentication_microservice.schemas import EstabelecimentoIn,EstabelecimentoOut
from http import HTTPStatus
from tortoise.expressions import Q
from tortoise.exceptions import DoesNotExist
from typing import Annotated


router = APIRouter(prefix='/estabelecimento',tags=['estabelecimento'])

@router.post('/',response_model=EstabelecimentoOut)
async def criar_estabelecimento(estabelecimento:EstabelecimentoIn):
    try:
        pacote = await Pacote.get(id=estabelecimento.pacote_id)
        await Estabelecimento.create(nome=estabelecimento.nome,icone_path="foto.png",pacote=pacote,cidade=estabelecimento.cidade)
        return HTTPStatus.CREATED
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Id do pacote não existe'
        )

#@router.get('/{id}')
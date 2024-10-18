from fastapi.routing import APIRouter
from fastapi import HTTPException,Depends,Request
from authentication_microservice.schemas import FuncionalidadeIn,FuncionalidadeOut,OrgaoIn,OrgaoOut
from authentication_microservice.models import Orgao,Estabelecimento
from http import HTTPStatus
from tortoise.exceptions import DoesNotExist
from uuid import UUID

router = APIRouter(prefix='/orgao',tags=['orgaos'])

@router.post('/',response_model=OrgaoOut)
async def create_orgao(o:OrgaoIn):
    try:
        estabelecimento = await Estabelecimento.get(id=o.estabelecimento_id)
        orgao = await Orgao.create(descricao=o.descricao,cnpj=o.cnpj,endereco=o.endereco,estabelecimento=estabelecimento)
        await orgao.fetch_related('estabelecimento')
        return orgao
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Id de documento não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro de servidor: {e}'
        )
    
@router.get('/{id}',response_model=OrgaoOut)
async def get_orgao(id:UUID):
    try:
        orgao = await Orgao.get(id=id)
        await orgao.fetch_related('estabelecimento')
        return orgao
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Id de documento não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro de servidor: {e}'
        )
    

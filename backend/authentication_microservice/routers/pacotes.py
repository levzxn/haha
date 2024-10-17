from fastapi.routing import APIRouter
from fastapi import HTTPException,Depends,Request
from authentication_microservice.schemas import FuncionalidadeIn,FuncionalidadeOut,PacoteIn,PacoteOut
from authentication_microservice.models import Funcionalidade,Pacote
from http import HTTPStatus
from tortoise.exceptions import DoesNotExist



router = APIRouter(prefix='/pacote',tags=['pacotes'])

@router.post('/',response_model=PacoteOut)
async def create_pacote(request:Request,pacote:PacoteIn):
    connection = request.state.db_connection
    try:
        p = await Pacote.create(using_db=connection)
        lista_funcs = [await Funcionalidade.get(id=func_id,using_db=connection) for func_id in pacote.func_ids]
        await p.funcionalidades.add(*lista_funcs,using_db=connection)
        await p.fetch_related('funcionalidades',using_db=connection)
        return p
    except DoesNotExist:
        await connection.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Id de funcionalidade não encontrado'
        )
    except Exception as e:
        await connection.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro interno: {e}'
        )
from fastapi.routing import APIRouter
from fastapi import Query,Request,HTTPException
from DOEMApi.models import Document,DiarioOficial
from DOEMApi.schemas import DocumentOut,UserOut
from DOEMApi.pdf_controller import create_pdf
import os,shutil,base64
from typing import List
from tortoise.exceptions import DoesNotExist
from uuid import UUID
from typing import Annotated
from http import HTTPStatus

router = APIRouter(prefix='/diario',tags=['diario_oficial'])

OUTPUT_DIR = "files/pdfs"

Tdoc_ids = Annotated[List[UUID],Query(...)]
@router.get('/gerar_diario/')
async def gerar_diario(request:Request,doc_ids:Tdoc_ids):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    titulo= 'Diario Oficial dia tal'
    file_path = os.path.join(OUTPUT_DIR,titulo+'.pdf')

    try:
        user_data = await request.state.user
        current_user = UserOut(**user_data)
        documents = [await Document.get(id=str(id)) for id in doc_ids]
        create_pdf([document.file_path for document in documents],file_path)
        with open(file_path,'rb') as stored_file:
            content = stored_file.read()
            encoded_content = base64.b64encode(content).decode("utf-8")
            diario = await DiarioOficial.create(titulo=titulo,file_path=file_path,chunks=encoded_content,sender=current_user.id)
        return {'content':encoded_content}
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de documento não encontrado'
        )
    except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Não foi possível processar o arquivo: {e}'
            )
    
@router.get('/{id}')
async def get_diario(id:int):
    try:
        diario = await DiarioOficial.get(id=id)
        return diario
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de diário não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro no servidor: {e}'
        )
from fastapi.routing import APIRouter
from fastapi import UploadFile,File,Form,Depends,Query,HTTPException,Request
from http import HTTPStatus 
from DOEMApi.models import Document,DiarioOficial
from DOEMApi.security import get_current_user
from DOEMApi.schemas import DocumentOut,UserOut
from DOEMApi.pdf_controller import create_pdf
import os,shutil,base64
from typing import List
from tortoise.exceptions import DoesNotExist
from uuid import UUID
from typing import Annotated

router = APIRouter(prefix='/docs',tags=['docs'])

UPLOAD_DIR = "fast_zero/files/uploads"
OUTPUT_DIR = "fast_zero/files/pdfs"

@router.post("/uploadfile/", status_code=HTTPStatus.OK,response_model=DocumentOut)
async def upload_file(request:Request,titulo:str=Form(...),file: UploadFile = File(...),orgao_id:UUID=Form(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read()) 
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"error": f"Erro ao salvar o arquivo: {str(e)}"})
    
    user_data = await request.state.user
    current_user = UserOut(**user_data)
    document = await Document.create(file_name=titulo,file_path=file_path,sender=current_user.id,orgao=orgao_id,tipo='Portaria')
    return document

@router.get('/file/{doc_id}/',status_code=HTTPStatus.OK)
async def get_document_content(doc_id:str):
    try:
        document = await Document.get(id=doc_id)
        with open(document.file_path,'rb') as stored_file:
            content = stored_file.read()
            encoded_content = base64.b64encode(content).decode("utf-8")
            return {'content':encoded_content}
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de documento não encontrado'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Não foi possivel processar o arquivo: {e}'
        )

@router.get('/all/',status_code=HTTPStatus.ACCEPTED,response_model=List[DocumentOut])
async def get_all_user_documents(request:Request):
    try:
        current_user = request.state.user
        documents = await Document.filter(sender=current_user.get('id'))
        return documents
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Não foi encontrado documentos desse usuário'
        )

Tdoc_ids = Annotated[List[UUID],Query(...)]
@router.get('/gerar_diario/')
async def gerar_diario(doc_ids:Tdoc_ids):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    file_path = os.path.join(OUTPUT_DIR,'DOEM 1.pdf')

    try:
        documents = [await Document.get(id=str(id)) for id in doc_ids]
        create_pdf([document.file_path for document in documents],file_path)
        with open(file_path,'rb') as stored_file:
            content = stored_file.read()
            encoded_content = base64.b64encode(content).decode("utf-8")
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
    

@router.get("/teste/", status_code=HTTPStatus.OK)
async def teste(request:Request):
    user = await request.state.user
    return user
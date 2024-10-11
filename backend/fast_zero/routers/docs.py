from fastapi.routing import APIRouter
from fastapi import UploadFile,File,Form,Depends,Query,HTTPException
from http import HTTPStatus 
from fast_zero.models import Document,User
from fast_zero.security import get_current_user
from fast_zero.schemas import DocumentOut
from fast_zero.pdf_controller import create_pdf
import os,shutil,base64
from typing import List
from tortoise.exceptions import DoesNotExist
from uuid import UUID

router = APIRouter(prefix='/docs',tags=['docs'])


UPLOAD_DIR = "fast_zero/files/uploads"
OUTPUT_DIR = "fast_zero/files/pdfs"

@router.post("/uploadfile/", status_code=HTTPStatus.OK,response_model=DocumentOut)
async def upload_file(titulo:str=Form(...),file: UploadFile = File(...),current_user: User = Depends(get_current_user)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read()) 
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"error": f"Erro ao salvar o arquivo: {str(e)}"})

    document = await Document.create(file_name=titulo,file_path=file_path,sender=current_user)
    
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
async def get_all_user_documents(current_user: User = Depends(get_current_user)):
    try:
        documents = await Document.filter(sender=current_user).select_related('sender')
        return documents
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Não foi encontrado documentos desse usuário'
        )


@router.get('/gerar_diario/')
async def gerar_diario(doc_ids:List[UUID]=Query(...)):
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
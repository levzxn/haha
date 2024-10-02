from fastapi.routing import APIRouter
from fastapi import UploadFile,File,Form
import os
from http import HTTPStatus
import shutil
from fast_zero.models import Document

router = APIRouter(prefix='/docs',tags=['docs'])


UPLOAD_DIR = "fast_zero/uploads/"

@router.post("/uploadfile/", status_code=HTTPStatus.OK)
async def upload_file(titulo:str=Form(...),file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document = Document(file_name=titulo,file_path=file_path)
    await document.save()
    
    return {'doc': file.filename}

@router.get('/{doc_name}/',status_code=HTTPStatus.OK)
async def get_document_content(doc_name:str):
    document = await Document.get(file_name=doc_name)
    with open(document.file_path,'rb') as stored_file:
        content = stored_file.read()
        return {'content':content}
        

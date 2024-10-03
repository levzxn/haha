from fastapi.routing import APIRouter
from fastapi import UploadFile,File,Form,Depends
from http import HTTPStatus 
from fast_zero.models import Document,User
from fast_zero.security import get_current_user
from fast_zero.schemas import DocumentOut
import os,shutil,base64
from typing import List

router = APIRouter(prefix='/docs',tags=['docs'])


UPLOAD_DIR = "fast_zero/uploads/"

@router.post("/uploadfile/", status_code=HTTPStatus.OK)
async def upload_file(titulo:str=Form(...),file: UploadFile = File(...),current_user: User = Depends(get_current_user)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document = Document(file_name=titulo,file_path=file_path,sender=current_user)
    await document.save()
    
    return {'doc': file.filename}

@router.get('/file/{doc_id}/',status_code=HTTPStatus.OK)
async def get_document_content(doc_id:int):
    document = await Document.get(id=doc_id)
    with open(document.file_path,'rb') as stored_file:
        content = stored_file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")
        return {'content':encoded_content}
        

@router.get('/all/',status_code=HTTPStatus.ACCEPTED,response_model=List[DocumentOut])
async def get_all_user_documents(current_user: User = Depends(get_current_user)):
    documents = await Document.filter(sender=current_user).select_related('sender')
    return documents



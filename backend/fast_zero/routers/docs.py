from fastapi.routing import APIRouter
from fastapi import UploadFile,File,Form,Depends
from http import HTTPStatus 
from fast_zero.models import Document,User
from fast_zero.security import get_current_user
import os,shutil,base64

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

'''@router.get('/{doc_name}/',status_code=HTTPStatus.OK)
async def get_document_content(doc_name:str):
    document = await Document.get(file_name=doc_name)
    with open(document.file_path,'rb') as stored_file:
        content = stored_file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")
        return {'content':encoded_content}'''
        

@router.get('/all/',status_code=HTTPStatus.ACCEPTED)
async def get_all_user_documents(current_user: User = Depends(get_current_user)):
    documents = await Document.filter(sender=current_user)
    return {'documents':documents}



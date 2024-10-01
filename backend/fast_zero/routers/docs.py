from fastapi.routing import APIRouter
from fastapi import UploadFile,File
import os
from http import HTTPStatus
import shutil
from fast_zero.models import Document

router = APIRouter(prefix='/docs',tags=['docs'])


UPLOAD_DIR = "uploads/"

@router.post("/uploadfile/", status_code=HTTPStatus.OK)
async def upload_file(file: UploadFile = File(...)):
    # Verifica se o diretório 'uploads' existe, se não, cria
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Salva o arquivo no diretório especificado
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Supondo que 'Document' seja um modelo e você está criando um registro no banco
    document = Document.create(file_path=file_path)
    
    return {'doc': file.filename}
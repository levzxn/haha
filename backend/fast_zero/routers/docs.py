from fastapi.routing import APIRouter
from fastapi import UploadFile,File,Form,Depends,Query,HTTPException
from http import HTTPStatus 
from fast_zero.models import Document,User
from fast_zero.security import get_current_user
from fast_zero.schemas import DocumentOut
from fast_zero.pdf_controller import create_pdf
import os,shutil,base64
from typing import List

router = APIRouter(prefix='/docs',tags=['docs'])


UPLOAD_DIR = "fast_zero/uploads/"

@router.post("/uploadfile/", status_code=HTTPStatus.OK)
async def upload_file(titulo:str=Form(...),file: UploadFile = File(...),current_user: User = Depends(get_current_user)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())  # Grava o conteúdo do arquivo no sistema de arquivos
    except Exception as e:
        return HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"error": f"Erro ao salvar o arquivo: {str(e)}"})

    document = Document(file_name=titulo,file_path=file_path,sender=current_user)
    await document.save()
    
    return {'doc': file.filename}

@router.get('/file/{doc_id}/',status_code=HTTPStatus.OK)
async def get_document_content(doc_id:int):
    try:
        document = await Document.get(id=doc_id)
        with open(document.file_path,'rb') as stored_file:
            content = stored_file.read()
            encoded_content = base64.b64encode(content).decode("utf-8")
            return {'content':encoded_content}
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de documento não encontrado'
        )
        

@router.get('/all/',status_code=HTTPStatus.ACCEPTED,response_model=List[DocumentOut])
async def get_all_user_documents(current_user: User = Depends(get_current_user)):
    documents = await Document.filter(sender=current_user).select_related('sender')
    return documents


@router.get('/gerar_diario/')
async def gerar_diario(doc_ids:List[int]=Query(...)):
    print('hi')
    documents = [await Document.get(id=id) for id in doc_ids]

    create_pdf([document.file_path for document in documents],'TesteDOC.pdf')
  
'''    #except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID de documento não encontrado'
        )'''
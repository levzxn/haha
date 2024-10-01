from fastapi.routing import APIRouter
from fastapi import UploadFile,File
from http import HTTPStatus
import shutil
from fast_zero.models import Document

router = APIRouter(prefix='/docs',tags=['docs'])


@router.post("/uploadfile/",status_code=HTTPStatus.OK)
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    document = Document.create(file_path=f"uploads/{file.filename}")
    return {'doc':file.filename}
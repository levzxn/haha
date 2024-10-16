from jwt import encode,decode,DecodeError, ExpiredSignatureError,PyJWTError
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from DOEMApi.schemas import TokenData
from http import HTTPStatus
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from typing import Annotated
import os
import requests


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        headers = {
        "Authorization": f"Bearer {token}"
        }
        response = requests.get(url='http://127.0.0.1:8001/user/me',headers=headers)
        user = response.json()
        return user
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'{e}'
        )
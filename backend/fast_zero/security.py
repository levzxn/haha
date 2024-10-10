from jwt import encode,decode,DecodeError, ExpiredSignatureError,PyJWTError
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from fast_zero.models import User
from fast_zero.schemas import TokenData
from http import HTTPStatus
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_ACCESS_TOKEN_EXPIRE_DAYS = 1
pwd_context = PasswordHash.recommended()


def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_enconde = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enconde.update({'exp': expire})
    encoded_jwt = encode(to_enconde,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=REFRESH_ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

T_token = Annotated[str,Depends(oauth2_scheme)]

async def get_current_user(token:T_token):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await User.get(username=token_data.username)
    
    if user:
        return user
    return credentials_exception

def decode_refresh_token(refresh_token: str):
    try:
        payload = decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return username
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
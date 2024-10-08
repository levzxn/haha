from fastapi.routing import APIRouter
from fastapi import HTTPException,Depends
from fast_zero.schemas import UserIn,UserOut
from fast_zero.models import User
from fast_zero.security import get_password_hash,get_current_user
from http import HTTPStatus
from tortoise.expressions import Q
from typing import Annotated


router = APIRouter(prefix='/user',tags=['user'])

T_User = Annotated[User,Depends(get_current_user)]

@router.get('/me',status_code=HTTPStatus.OK,response_model=UserOut)
async def get_nomes(current_user: T_User):
    return current_user

@router.post('/',status_code=HTTPStatus.CREATED)
async def create_user(user:UserIn):
        try:
            db_user = await User.get(Q(username=user.username) | Q(email=user.email))
            
        except:
            hashed_password = get_password_hash(user.password)
            db_user = User(username=user.username,email=user.email,password=hashed_password)
            await db_user.save()
            return db_user
        
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username alredy exists"
                )
        if db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Email adress alredy exists"
                )

@router.put('/{user_id}',status_code=HTTPStatus.OK,response_model=UserOut)
async def update_user(user_id:int,updated_user:UserIn,current_user: T_User):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    current_user.username = updated_user.username
    current_user.email = updated_user.email
    current_user.password = get_password_hash(updated_user.password)
    await current_user.save()
    return current_user

@router.delete('/{user_id}',status_code=HTTPStatus.OK)
async def delete_user(user_id:int,current_user: T_User) :
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    await current_user.delete()
    return {"user_deleted":current_user.username}   

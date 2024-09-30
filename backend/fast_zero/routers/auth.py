from fastapi.routing import APIRouter
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fast_zero.models import User
from fast_zero.security import verify_password,create_acess_token
from http import HTTPStatus

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post('/token',status_code=HTTPStatus.OK)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        db_user = await User.get(username=form_data.username)
    except:       
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Username doesn't exist"
        )  
    if verify_password(form_data.password,db_user.password):
        acess_token = create_acess_token(data={"sub":form_data.username})
        return {'acess_token':acess_token,'token_type':'bearer'}
    else:
        raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid password"
            )
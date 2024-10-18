from fastapi.routing import APIRouter
from fastapi import HTTPException,Depends,Request
from authentication_microservice.schemas import UserIn,UserOut,UptadedUser,EmailIn,EmailOut,TokenResetIn
from authentication_microservice.models import User,Estabelecimento,Orgao,Pacote,Funcionalidade,TokenReset
from authentication_microservice.security import get_password_hash,get_current_user
from http import HTTPStatus
from tortoise.expressions import Q
from tortoise.exceptions import DoesNotExist,IntegrityError
from typing import Annotated
from uuid import UUID
import requests
from datetime import datetime,timedelta
import pytz

router = APIRouter(prefix='/user',tags=['user'])

T_User = Annotated[User,Depends(get_current_user)]

@router.get('/me',status_code=HTTPStatus.OK,response_model=UserOut)
async def get_nomes(current_user: T_User):
    await current_user.fetch_related('estabelecimento')
    return current_user

@router.post('/',status_code=HTTPStatus.CREATED,response_model=UserOut)
async def create_user(user:UserIn):
        db_user:User = await User.get_or_none(Q(username=user.username) | Q(email=user.email))
        
        if db_user is not None:
            if db_user.username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Nome de usuário já existe"
                    )
            elif db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Email já cadastrado em outra conta"
                ) 
        else:
            hashed_password = get_password_hash(user.password)
        try:
            estabelecimento = await Estabelecimento.get(id=user.estabelecimento)
            db_user = await User.create(
                username=user.username,email=user.email,password=hashed_password,
                is_admin=user.is_admin,estabelecimento=estabelecimento
                                        )
            return db_user
        except DoesNotExist:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Id de estabelecimento não existe'
            )
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Erro ao criar usuário: {e}'
            )

@router.put('/{user_id}/',status_code=HTTPStatus.OK,response_model=UserOut)
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

@router.patch('/{user_id}/')
async def update_user_fields(request:Request,user_id:UUID,updated_user:UptadedUser):
    try:
        current_user:User = await request.state.user
        if current_user.id == user_id or current_user.is_admin:
            user = await User.get(id=user_id)
            await user.update_from_dict(updated_user.model_dump(exclude_none=True))
            return user
        else:
            raise HTTPException(
                status_code=HTTPStatus.METHOD_NOT_ALLOWED,
                detail='Sem permissões para atualizar usuário'
            )
    except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Erro ao atualizar usuário: {e}'
            )

@router.delete('/{user_id}/',status_code=HTTPStatus.OK,response_model=UserOut)
async def delete_user(user_id:UUID,current_user: T_User) :
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    await current_user.delete()
    return current_user   

fuso_horario = pytz.timezone('America/Sao_Paulo')

@router.post('/password_reset/')
async def reset_my_password(email:EmailIn):
    try:
        user = await User.get(email=email.email_adress)
        token = await TokenReset.get_or_none(user=user)
        if token is None:
            token = await TokenReset.create(user=user,expires_at=datetime.now(fuso_horario)+timedelta(minutes=15))
            email_out = EmailOut(email=user.email,subject='Recuperação de senha',keys={'token':str(token.id)})
            response = requests.post(url='http://127.0.0.1:8002/email/send/',json=email_out.model_dump())
            return response.json()
        else:
            await token.delete()
            email = EmailIn(email_adress=user.email)
            return await reset_my_password(email=email)
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Email não vinculado a nenhum usuário'
        )
    except Exception as e:
        raise e


@router.post('/check_reset_token/')
async def get_user_by_token(token:TokenResetIn):
    try:
        token_model = await TokenReset.get(id=token.token_id)
        if datetime.now(fuso_horario) < token_model.expires_at: 
            user = await token_model.user
            await token_model.delete()
            return user.id
        else:
            await token_model.delete()
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Token expirado'
            )
    except DoesNotExist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Token inválido'
        )
    except Exception as e:
        raise e
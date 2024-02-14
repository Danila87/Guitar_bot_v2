from fastapi import APIRouter, HTTPException

from pydantic_schemes import schemes

from database import models
from database.Query import Query as db

import datetime

router_service = APIRouter(
    prefix='service',
    tags=['service']
)


@router_service.post('/request')
async def request(data: schemes.RequestSong):

    if await db.insert_data(model=models.Requests,
                            user_id=data.user_id,
                            song_id=data.song_id,
                            date=datetime.datetime.now()):

        raise HTTPException(status_code=201, detail='Запрос обработан')

    raise HTTPException(status_code=400, detail='Произошла ошибка')


@router_service.post('/check_user', response_model=schemes.User)
async def check_user(user: schemes.User):

    if await db.get_data_by_filter(model=models.Users, verify=True, telegram_id=user.telegram_id):
        raise HTTPException(status_code=400, detail='Пользователь существует')

    await db.insert_data(model=models.Users,
                         telegram_id=user.telegram_id,
                         first_name=user.first_name,
                         ast_name=user.last_name,
                         nickname=user.nickname)

    raise HTTPException(status_code=201, detail='Пользователь создан')
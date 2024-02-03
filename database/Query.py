from typing import Union

from .models import CategorySong
from .connection import db_session

from sqlalchemy import select

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload

from fastapi.encoders import jsonable_encoder


class Query:

    @staticmethod
    async def get_all_data(model) -> dict:

        async with db_session() as session:

            query = select(model)
            result = await session.execute(query)

            data = result.scalars().all()

            return jsonable_encoder(data)

    @staticmethod
    async def get_data_by_id(model, model_id: int, encode: bool = True,) -> dict:

        async with db_session() as session:

            query = select(model).filter(model.id == model_id)

            result = await session.execute(query)
            data = result.scalars().one()

            if encode:
                return jsonable_encoder(data)

            return data

    @staticmethod
    async def delete_data_by_id(model, model_id: int) -> bool:

        async with db_session() as session:

            data = await Query.get_data_by_id(model=model, model_id=model_id, encode=False)

            await session.delete(data)
            await session.commit()

            return True

    @staticmethod
    async def get_data_by_filter(model, verify: bool = False, **kwargs) -> Union[dict, bool]:

        async with db_session() as session:

            query = select(model).filter_by(**kwargs)
            result = await session.execute(query)

            data = result.scalars().all()

            if verify:

                if len(data) == 0:
                    return False

                return True

            return jsonable_encoder(data)

    @staticmethod
    async def insert_data(model, **kwargs) -> bool:

        async with db_session() as session:

            data = model(**kwargs)
            session.add(data)

            await session.commit()

            return True

    @staticmethod
    async def update_data_by_id(model, model_id: int):
        pass
    
    @staticmethod
    async def get_all_songs_by_category():

        async with db_session() as session:

            query = select(CategorySong).options(selectinload(CategorySong.songs))

            result = await session.execute(query)
            result = result.scalars().all()

            return jsonable_encoder(result)
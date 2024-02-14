from __future__ import annotations

from .models import CategorySong, Songs
from .connection import db_session

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from fastapi.encoders import jsonable_encoder

from fuzzywuzzy import fuzz


class Query:

    @staticmethod
    async def get_all_data(model) -> dict:

        async with db_session() as session:

            query = select(model)
            result = await session.execute(query)

            data = result.scalars().all()

            return jsonable_encoder(data)

    @staticmethod
    async def get_data_by_id(model, model_id: int, encode: bool = True,) -> dict | bool:

        async with db_session() as session:

            query = select(model).filter(model.id == model_id)

            result = await session.execute(query)
            data = result.scalar_one_or_none()

            if not data:
                return False

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
    async def get_data_by_filter(model, verify: bool = False, **kwargs) -> dict | bool:

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

    @staticmethod
    async def search_all_songs_by_title(title_song: str) -> list[dict] | bool:

        all_songs = await Query.get_all_data(model=Songs)
        result_songs = []

        for song in all_songs:

            if fuzz.WRatio(song['title'], title_song) < 75:

                continue

            result_songs.append(
                {
                    'id_song': song['id'],
                    'title_song': song['title']
                }
            )

        if not result_songs:
            return False

        return result_songs

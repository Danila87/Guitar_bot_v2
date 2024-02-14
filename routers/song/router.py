from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from pydantic_schemes.schemes import *

from database import models
from database.Query import Query as db

song_router = APIRouter(prefix='/song', tags=['all_song_methods'])


async def verify_song(song: Song) -> Song:  # Проверять есть ли уже такая песня в БД

    if await db.get_data_by_filter(model=models.Songs, verify=True, title=song.title):
        raise HTTPException(status_code=400, detail='Такая песня уже существует')

    return song


async def verify_category(category: CategorySong) -> CategorySong:  # Проверять есть ли уже такая категория в БД

    if await db.get_data_by_filter(model=models.CategorySong, verify=True, category=category.category):
        raise HTTPException(status_code=400, detail='Данная категория существует')

    return category


def refactor_text(text: str) -> str:

    formatted_text = text.replace('\n', '\\n')

    return formatted_text


@song_router.get('/songs/by_category', tags=['song', 'category'])
async def get_songs_by_category():

    songs = await db.get_all_songs_by_category()

    return songs


@song_router.get('/songs', tags=['song'])
async def get_songs() -> list[dict]:

    songs = await db.get_all_data(model=models.Songs)

    return songs


@song_router.get('/songs/{title_song}', tags=['song'])
async def search_songs_by_title(title_song: str):

    songs = await Query.search_all_songs_by_title(title_song=title_song)

    return songs


@song_router.post('/song', tags=['song'])
async def insert_song(song: Song = Depends(verify_song)):

    song.text = refactor_text(text=song.text)

    if await db.insert_data(model=models.Songs,
                            title=song.title,
                            title_search=song.title_search,
                            text=song.text,
                            file_path=song.file_path,
                            category=song.category):

        return HTTPException(status_code=201, detail='Песня успешно добавлена!')

    return HTTPException(status_code=400, detail='Произошла ошибка на сервере')


@song_router.get('/song/{song_id}', tags=['song'])
async def get_song(song_id: int) -> dict | bool:

    song = await db.get_data_by_id(model=models.Songs, model_id=song_id)
    if not song:
        raise HTTPException(status_code=400, detail='Песни не существует')

    return song


@song_router.put('/song/{song_id}', tags=['song'])
async def update_song_by_id(song_id: int, song: Song):
    pass


@song_router.delete('/song/{song_id}', tags=['song'])
async def delete_song_by_id(song_id: int):

    if await db.delete_data_by_id(model=models.Songs, model_id=song_id):
        return HTTPException(status_code=200, detail='Песня успешно удалена')

    return HTTPException(status_code=500, detail='Возникли проблемы при удалении')


@song_router.get('/categories', tags=['category'], response_model=list[CategorySong])
async def get_all_categories() -> dict:

    categories = await db.get_all_data(model=models.CategorySong)

    return categories


@song_router.post('/category', tags=['category'])
async def insert_category(category: CategorySong = Depends(verify_category)):

    if await db.insert_data(model=models.CategorySong, category=category.category):
        return HTTPException(status_code=201, detail='Категория успешно добавлена')


@song_router.get('/categories/{category_id}', tags=['category'], response_model=CategorySong)
async def get_category_by_id(category_id: int) -> dict:

    category = await db.get_data_by_id(model=models.CategorySong, model_id=category_id)

    return category


@song_router.put('/categories/{category_id}', tags=['category'])
async def update_category_by_id(category_id: int):

    pass


@song_router.delete('/categories/{category_id}', tags=['category'])
async def delete_category_by_id(category_id: int):

    if await db.delete_data_by_id(model=models.CategorySong, model_id=category_id):
        return HTTPException(status_code=200, detail='Категория успешно удалена')

    return HTTPException(status_code=500, detail='Произошла ошибка на сервере')


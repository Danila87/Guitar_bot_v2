from pydantic import BaseModel, field_validator

from database.Query import Query
from database.models import CategorySong


class Song(BaseModel):

    title: str
    title_search: str
    text: str
    file_path: str = None
    category: int = None  # Это внешний ключ, посмотреть как сюда передавать только корректные значения

    @classmethod
    @field_validator('category')
    async def validate_category(cls, value):

        if await Query.get_data_by_id(model=CategorySong, id=value):
            return value

        raise ValueError('Категория не найдена в БД')


class CategorySong(BaseModel):

    category: str

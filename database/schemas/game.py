

from datetime import date
from typing import Optional
from pydantic import Field, validator
from sqlmodel import SQLModel


class GameSchema(SQLModel, table=False):
    appid: Optional[int] = None
    name: Optional[str] = None
    release_date: date = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    achievements: Optional[bool] = None
    positive_ratings: Optional[int] = None
    negative_ratings: Optional[int] = None
    average_playtime: Optional[float] = None
    median_playtime: Optional[float] = None
    price: Optional[float] = None
    platforms: Optional[list[str]] = []
    categories: Optional[list[str]] = []
    genres: Optional[list[str]] = []
    steampsy_tags: Optional[list[str]] = []
    owners: Optional[str] = None

    @validator('platforms', 'categories', 'genres', 'steampsy_tags', pre=True)
    @classmethod
    def split_data(cls, v: str):
        if v and type(v) is str:
            return v.split(';')

        return v
    
    @validator('appid', 'positive_ratings', 'negative_ratings', pre=True)
    @classmethod
    def transform_int_data(cls, v: str):
        if v and type(v) is str and v.isnumeric():
            return int(v)
    
        return v
    
    @validator('average_playtime', 'median_playtime', 'price', pre=True)
    @classmethod
    def transform_float_data(cls, v: str):
        if v and type(v) is str and v.isnumeric():
            return float(v)
    
        return v
    
    @validator('achievements', pre=True)
    def validate_boolean(cls, v):
        if v and type(v) is str:
            return v == 'true'
        elif type(v) == int:
            return bool(v)
    
        return v
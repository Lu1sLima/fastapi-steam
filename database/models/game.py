from typing import Optional
from pydantic import validator
from sqlmodel import SQLModel, Field
from datetime import date


class Game(SQLModel, table=True):
    __tablename__ = 'games'

    appid: int = Field(alias="appid", default=None, primary_key=True)
    name: str = Field(unique=True)
    release_date: date
    developer: str
    publisher: str
    platforms: str
    required_age: int
    steamspy_tags: Optional[str]
    categories: str
    genres: str
    achievements: int
    positive_ratings: int
    negative_ratings: int
    average_playtime: float
    median_playtime: float
    owners: str
    price: float


    @validator('platforms', 'categories', 'genres', 'steamspy_tags', pre=True)
    @classmethod
    def split_data(cls, v: str, values, config, field):
        if v and type(v) is list:
            return ';'.join(v)

        return None
    
    # @validator('appid', 'positive_ratings', 'negative_ratings', pre=True)
    # @classmethod
    # def transform_int_data(cls, v: str):
    #     if v and type(v) is str and v.isnumeric():
    #         return int(v)
    
    #     return v
    
    # @validator('average_playtime', 'median_playtime', 'price', pre=True)
    # @classmethod
    # def transform_float_data(cls, v: str):
    #     if v and type(v) is str and v.isnumeric():
    #         return float(v)
    
    #     return v
    
    # @validator('achievements', pre=True)
    # def validate_boolean(cls, v):
    #     if v and type(v) is str:
    #         return v == 'true'
    #     elif type(v) == int:
    #         return bool(v)
    
    #     return v
from datetime import date
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, validator

class Gender(str, Enum):
    male = "male"
    female = "female"

class Book(BaseModel):
    id: UUID = uuid4()
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    rating: int = Field(gt=-1, lt=101)
    published_date: date
    available: bool = True

    @validator("published_date")
    def verify_published_date(cls, v):
        if v > date.today():
            raise ValueError("date of publish cannot exceed today's date")
        return v

class User(BaseModel):
    id: UUID = uuid4()
    name: str = Field(min_length=1)
    age: int = Field(gt=0)
    gender: Gender
    borrowed_book: Book | None = None
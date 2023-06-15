from datetime import date
from enum import Enum
from pydantic import BaseModel, Field, validator

class Gender(str, Enum):
    male = "male"
    female = "female"

class BookBase(BaseModel):
    title: str
    author: str
    rating: int = Field(gt=-1, lt=101)
    published_date: date

    @validator("published_date")
    def verify_published_date(cls, v):
        if v > date.today():
            raise ValueError("date of publish cannot exceed today's date")
        return v
    
class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_available: bool
    borrower_id: int | None = None

    class Config:
        orm_mode = True

class UpdateBook(BaseModel):
    is_available: bool 


class UserBase(BaseModel):
    email: str
    name: str
    age: int = Field(gt=0)
    gender: Gender

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    borrowed_books: list[Book] | None = []

    class Config:
        orm_mode = True
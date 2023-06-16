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
    title: str | None = None
    author: str | None = None
    rating: int | None = Field(default=None, gt=-1, lt=101)
    published_date: date | None = None
    is_available: bool | None = None
    borrower_id: int | None = None


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

class UpdateUser(BaseModel):
    email: str | None = None
    name: str | None = None
    age: int | None = Field(default=None, gt=0)
    gender: Gender | None = None
    borrowed_books: list[Book] | None = None
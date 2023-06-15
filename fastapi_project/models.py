from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Gender(str, Enum):
    male = "male"
    female = "female"
    
class Book(BaseModel):
    id: UUID = uuid4()
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    rating: int = Field(gt=-1, lt=101)
    published_date: datetime.date = Field(lt=date.today)

class User(BaseModel):
    id: UUID = uuid4()
    name: str = Field(min_length=1)
    age: int = Field(gt=0)
    gender: Gender
    borrowed_books: list[Book] | None = []

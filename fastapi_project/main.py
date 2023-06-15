from datetime import date
import uvicorn
from uuid import uuid4
from fastapi import FastAPI
from .schemas import Gender, User, Book
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . import models

app = FastAPI()


# db_books: list[Book] = [
#     Book(id=uuid4(), title="Jack and Jill", author="Louisa May Alcott", rating=99, published_date=date(2022, 1, 2)),
#     Book(id=uuid4(), title="Jack and the Beanstalk", author="Joseph Jacobs", rating=85, published_date=date(2022, 1, 2))
# ]

# db_users: list[User] = [
#     User(id=uuid4(), name="Aliff", age=20, gender=Gender.male, borrowed_books=[db_books[0], db_books[1]]),
#     User(id=uuid4(), name="Hana", age=21, gender=Gender.female),
# ]

@app.get("/")
def root():
    return {"Message" : "Home Page"}

@app.get("/users")
def get_users():
    return db_users
    
def main():
    """Launched with `poetry run start`"""
    uvicorn.run("fastapi_project.main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()
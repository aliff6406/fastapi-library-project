from datetime import date
import uvicorn
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException
from . import crud, models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

description = """
## Books

You are able to:

* **Create books**
* **Read books**

## Users

You are able to:

* **Create users**
* **Read users**
"""

tags_metadata = [
    {
        "name": "books",
        "description": "Operations with books."
    },
    {
        "name": "users",
        "description": "Operations with users."
    }
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LibraryApp",
    description=description,
    openapi_tags=tags_metadata
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"Message" : "Home Page"}

@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already Registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    return db_user

@app.post("/books/", response_model=schemas.Book, tags=["books"])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already Registered")
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book], tags=["books"])
def read_books(db: Session = Depends(get_db)):
    books = crud.get_books(db)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book, tags=["books"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    return db_book

def main():
    """Launched with `poetry run start`"""
    uvicorn.run("fastapi_project.main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()
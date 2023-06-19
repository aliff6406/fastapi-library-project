from datetime import date
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from . import crud, models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

description = """
## Books

You are able to:

* **Create books**.
* **Read books**.
* **Update books**.

## Users

You are able to:

* **Create users**.
* **Read users**.
* **Update users borrowed books** (_not implemented_).
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

@app.put("/users/{user_id}", response_model=schemas.User, tags=["users"])
def user_borrow_book_by_id(user_id: int, book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book ID {book_id} : Does not exist")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} : Does not exist")
    db_book_to_update = crud.update_book_availability(db=db, book_id=book_id, borrower_id=user_id)
    return crud.update_user_borrowed_book(db=db, user_id=user_id, book_id=book_id)

@app.delete("/users/{user_id}", response_model=dict(), tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} : Does not exist")
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return deleted_user

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

@app.put("/books/{book_id}", response_model=schemas.Book, tags=["books"])
def update_book(book_id: int, book: schemas.UpdateBook, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book ID {book_id} : Does not exist")
    return crud.update_book(db=db, book_id=book_id, book=book)

def main():
    """Launched with `poetry run start`"""
    uvicorn.run("fastapi_project.main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()
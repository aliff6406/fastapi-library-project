from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

def update_user_borrowed_book(db: Session, user_id: int, book_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.borrowed_book_id = book_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: schemas.UserCreate):
     db_user = models.User(**user.dict())
     db.add(db_user)
     db.commit()
     db.refresh(db_user)
     return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {f"User {user_id}" : "Successfully Deleted"}

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_title(db: Session, title: str):
     return db.query(models.Book).filter(models.Book.title == title).first()

def get_books(db: Session):
    return db.query(models.Book).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book_availability(db: Session, book_id: int, borrower_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_book.is_available = False
    db_book.borrower_id = borrower_id
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.UpdateBook):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    for var, value in vars(book).items():
        setattr(db_book, var, value) if value or str(value) == 'False' else None
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

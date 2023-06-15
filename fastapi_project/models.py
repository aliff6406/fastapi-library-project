from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    author = Column(String)
    rating = Column(Integer)
    published_date = Column(Date)
    is_available = Column(Boolean, default=True)
    borrower_id = Column(Integer, ForeignKey("User.id"))
    
    borrower = relationship("User", back_populates="book")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)

    book = relationship("Book", back_populates="borrower")
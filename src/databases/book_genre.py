# coding=utf-8

from sqlalchemy import Column, Integer, String, Date, ForeignKey

from base import Base


class BookGenre(Base):
    __tablename__ = 'book_genres'
    
    id = Column(Integer, primary_key=True, index=True)
    
    book_id = Column(Integer, ForeignKey('books.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
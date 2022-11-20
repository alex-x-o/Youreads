# coding=utf-8

from sqlalchemy import Column, String, Integer, Float

from base import Base
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    
    videos = relationship('Video', secondary='book_videos', backref='Book')
    # readers = relationship('Reader', secondary='book_readers')
    genres = relationship('Genre', secondary='book_genres', backref='Book')

    cover = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    avg_rating = Column(Float, nullable=False)
    num_ratings = Column(Integer, nullable=False)
    num_pages = Column(Integer)
    book_format = Column(String)
    url = Column(String, nullable=False)

    def __init__(self, cover, title, author, avg_rating, num_ratings, num_pages, book_format, url):
        self.cover = cover
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.num_ratings = num_ratings
        self.num_pages = num_pages
        self.book_format = book_format
        self.url = url

# coding=utf-8

from sqlalchemy import Column, String, Integer

from base import Base
from sqlalchemy.orm import relationship


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    
    # books = relationship('Book', secondary='book_genres', backref='Genre')
    
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

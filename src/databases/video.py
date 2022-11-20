# coding=utf-8

from sqlalchemy import Column, String, Integer, Float, Date

from base import Base
from sqlalchemy.orm import relationship


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    
    # books = relationship('Book', secondary='book_videos')
    
    title = Column(String(100), nullable=False)
    description = Column(String(5000), nullable=False)
    duration = Column(Integer, nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer)
    comment_count = Column(Integer, nullable=False)
    published_date = Column(Date, nullable=False)
    published_day = Column(String(9), nullable=False)

    def __init__(self, title, description, duration, view_count, like_count, comment_count, published_date, published_day):
        self.title = title
        self.description = description
        self.duration = duration
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count
        self.published_date = published_date
        self.published_day = published_day

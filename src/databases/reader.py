# coding=utf-8

from sqlalchemy import Column, String, Integer

from base import Base
from sqlalchemy.orm import relationship

class Reader(Base):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    
    # books = relationship('Book', secondary='book_readers')
    
    channel_name = Column(String(100), nullable=False)
    sub_count = Column(Integer, nullable=False)
    view_count = Column(Integer, nullable=False)
    video_count = Column(Integer, nullable=False)
    goodreads_link = Column(String)
    youtube_link = Column(String, nullable=False)
    book_count = Column(Integer)

    def __init__(self, channel_name, sub_count, view_count, video_count, goodreads_link, youtube_link, book_count):
        self.channel_name = channel_name
        self.sub_count = sub_count
        self.view_count = view_count
        self.video_count = video_count
        self.goodreads_link = goodreads_link
        self.youtube_link = youtube_link
        self.book_count = book_count

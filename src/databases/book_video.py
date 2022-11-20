# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey

from base import Base


class BookVideo(Base):
    __tablename__ = 'book_videos'
    
    id = Column(Integer, primary_key=True, index=True)
    
    book_id = Column(Integer, ForeignKey('books.id'))
    video_id = Column(Integer, ForeignKey('videos.id'))
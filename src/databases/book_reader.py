# coding=utf-8

from sqlalchemy import Column, Integer, String, Date, CheckConstraint, ForeignKey

from base import Base
from sqlalchemy.orm import relationship, backref

from book import Book
from reader import Reader

class BookReader(Base):
    __tablename__ = 'book_readers'
        
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    reader_id = Column(Integer, ForeignKey('readers.id'), primary_key=True)
    
    book = relationship(Book, backref=backref('book_assoc'))
    reader = relationship(Reader, backref=backref('reader_assoc'))
    
    rating = Column(Integer)
    date_started = Column(Date)
    date_read = Column(Date)
    read_count = Column(Integer, nullable=False)
    review = Column(String)
    bookshelf = Column(String, nullable=False)
    
    __table_args__ = ( 
        CheckConstraint(bookshelf.in_(['read', 'currently reading', 'want to read'])), 
        CheckConstraint(date_started <= date_read)            
    )
    
    def __init__(self, book, reader, rating, date_started, date_read, read_count, review, bookshelf):
        self.book = book
        self.reader = reader
        self.rating = rating
        self.date_started = date_started
        self.date_read = date_read
        self.read_count = read_count
        self.review = review
        self.bookshelf = bookshelf

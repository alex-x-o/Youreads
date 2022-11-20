# coding=utf-8

# 1 - imports
from datetime import datetime

from base import Session, engine, Base
from book import Book
from video import Video
from reader import Reader
from genre import Genre
from book_video import BookVideo
from book_reader import BookReader
from book_genre import BookGenre

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - create books
book_1 = Book('https://i.gr-assets.com/images/S/compressed.ph', 'Dream of the Divided Field: Poems', '., Yanyi', 4.01, 167, 96, 'Paperback', 'https://goodreads.com/book/show/58133514-dream')
book_2 = Book('https://i.gr-assets.com/images/S/compressed.ph', 'Winter Recipes from the Collective', 'Glück, Louise', 4.03, 1470, 46, 'Hardcover', 'https://goodreads.com/book/show/56269266-winte')
book_3 = Book('https://i.gr-assets.com/images/S/compressed.ph', 'Bless the Daughter Raised by a Voice in Her He', 'Shire, Warsan', 4.29, 2785, 96, 'Paperback', 'https://goodreads.com/book/show/55835966-bless')

# 5 - create readers
reader_1 = Reader('Jack Edwards', 1150000, 77692524, 293, 'https://www.goodreads.com/author/show/20013214', 'https://youtube.com/kfdjgldf', 1234)
reader_2 = Reader('The Book Leo', 192000, 11516872, 291, 'https://www.goodreads.com/user/show/23388825-l', 'https://youtube.com/itioerngv,', 234)
reader_3 = Reader('Jack In The Books', 371000, 22285851, 124, None, 'https://youtube.com/klgjfdkljgdfk', 333)

# 5 - create videos
video_1 = Video('i read popular books to tell you which ones ar', '[ad] head to http://squarespace.com/jackedward', 1266, 259299, 15313, 430, datetime.strptime('2022-10-31', '%Y-%m-%d'), 'Monday')
video_2 = Video('i read more books Harry Styles recommended and', '[ad] sign up to Milanote for free with no time', 847, 327281, 21578, 617, datetime.strptime('2022-10-27', '%Y-%m-%d'), 'Thursday')
video_3 = Video('Favourite Book Couples | OTP book tag', 'All my favourite book couples and OTP', 550, 15836, 422, 109, datetime.strptime('2016-09-01', '%Y-%m-%d'), 'Thursday')

# [Poetry, Queer, LGBT]
# [Poetry, Contemporary, Nonfiction, American]
# [Poetry, Feminism, Nonfiction, Africa, Somalia]

# 5 - create genres
genre_1 = Genre('Poetry')
genre_2 = Genre('Queer')
genre_3 = Genre('LGBT')
genre_4 = Genre('Contemporary')
genre_5 = Genre('Nonfiction')
genre_6 = Genre('American')
genre_7 = Genre('Feminism')
genre_8 = Genre('Africa')
genre_9 = Genre('Somalia')

# 6 - add genres to books
book_1.genres = [genre_1, genre_2, genre_3]
book_2.genres = [genre_1, genre_4, genre_5, genre_6]
book_3.genres = [genre_1, genre_7, genre_5, genre_8, genre_9]

# add readers to books
book_reader1 = BookReader(book_1, reader_1, 2, datetime.strptime('17/11/2022', '%d/%m/%Y'), datetime.strptime('18/11/2022', '%d/%m/%Y'), 1, None, 'read')
book_reader2 = BookReader(book_2, reader_1, 3, datetime.strptime('17/11/2022', '%d/%m/%Y'), datetime.strptime('17/11/2022', '%d/%m/%Y'), 1, None, 'read')
book_reader3 = BookReader(book_3, reader_1, 4, datetime.strptime('17/11/2022', '%d/%m/%Y'), datetime.strptime('17/11/2022', '%d/%m/%Y'), 1, None, 'read')

# add videos to books
book_1.videos = [video_1, video_2]
book_2.videos = [video_3]

# 9 - persists data
session.add_all([book_reader1, book_reader2, book_reader3])

session.add_all([video_1, video_2, video_3])

session.add_all([genre_1, genre_2, genre_3, genre_4, genre_5, genre_6, genre_7, genre_8, genre_9])

# 10 - commit and close session
session.commit()
session.close()
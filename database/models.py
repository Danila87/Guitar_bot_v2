from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import ForeignKey, Column, String, Integer, Date


class Base(DeclarativeBase):
    pass


class Songs(Base):

    __tablename__ = 'Songs'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    title_search = Column(String, index=True)
    text = Column(String(5000))
    file_path = Column(String, nullable=True)

    category = Column(Integer, ForeignKey('CategorySong.id', ondelete='SET NULL'), nullable=True)
    rel_category = relationship('CategorySong', back_populates='songs')


class CategorySong(Base):

    __tablename__ = 'CategorySong'

    id = Column(Integer, primary_key=True)
    category = Column(String(50))

    songs = relationship('Songs', back_populates='rel_category')


class Requests(Base):

    __tablename__ = 'Requests'

    id = Column(Integer, primary_key=True)

    id_user = Column(Integer, ForeignKey('Users.id'))
    id_song = Column(Integer, ForeignKey('Songs.id'))

    date = Column(Date)


class Users(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    nickname = Column(String)

    reviews = relationship('Reviews', back_populates='users')


class SongBooks(Base):

    __tablename__ = 'SongBooks'

    id = Column(Integer, primary_key=True)

    name = Column(String(50))
    file_path = Column(String(100))


class Reviews(Base):

    __tablename__ = 'Reviews'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('Users.id'))

    text_review = Column(String(500))
    looked_status = Column(Integer)
    created_data = Column(Date)

    users = relationship('Users', back_populates='reviews')


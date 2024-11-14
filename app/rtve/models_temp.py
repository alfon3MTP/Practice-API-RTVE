from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base

# ---- Refactor SQLAlchemy Models ----

class PubState(Base):
    __tablename__ = "pub_state"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    #programs = relationship("Program", back_populates="pubState")


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    htmlUrl = Column(String, nullable=True)
    uid = Column(String, nullable=True)

    programs = relationship("Program", back_populates="channel")


# Association table for many-to-many relationship between Program and Genres
program_genre = Table(
    'program_genre', Base.metadata,
    Column('program_id', Integer, ForeignKey('program.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.id'), primary_key=True)
)

class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    generoInf = Column(String, nullable=True)
    generoInfUid = Column(String, nullable=True)
    generoId = Column(String, nullable=True)

    programs = relationship("Program", secondary=program_genre, back_populates="genres")


class Program(Base):
    __tablename__ = "program"

    id = Column(Integer, primary_key=True, index=True)
    htmlUrl = Column(String, nullable=True)
    uid = Column(String, nullable=True)
    name = Column(String, nullable=True)
    language = Column(String, nullable=True)
    description = Column(String, nullable=True)
    emission = Column(String, nullable=True)
    publicationDate = Column(DateTime(timezone=True))

    channel_id = Column(Integer, ForeignKey("channel.id"))
    pub_state_id = Column(Integer, ForeignKey("pub_state.id"))

    channel = relationship("Channel", back_populates="programs")
    pubState = relationship("PubState", back_populates="programs")
    genres = relationship("Genre", secondary=program_genre, back_populates="programs")

from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from sqlalchemy import UniqueConstraint

# ---- Refactor SQLModel

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.database import Base

## Pydantic Model (This is not necessary, it's just to practice)

## RTVE API Response

class TVPubState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: Optional[str] = None
    description: Optional[str] = None

class TVChannel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = None
    htmlUrl: Optional[str] = None
    uid: Optional[str] = None

    programs: List["TVProgram"] = Relationship(back_populates="channel")

class TVProgramGenreLink(SQLModel, table=True):
    program_id: Optional[int] = Field(default=None, foreign_key="tvprogram.id", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="tvgenres.id", primary_key=True)


class TVGenres(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    generoInf: Optional[str] = None
    generoInfUid: Optional[str] = None
    generoId: Optional[str] = None

    programs: List["TVProgram"] = Relationship(
        back_populates="genres",
        link_model=TVProgramGenreLink  # Corrected by removing quotes
    )

class TVProgram(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    htmlUrl: str
    uid: str
    name: str
    language: Optional[str] = None
    description: Optional[str] = None
    emission: Optional[str] = None
    publicationDate: Optional[datetime] = None

    # Media details
    orden: Optional[int] = None
    imageSEO: Optional[str] = None
    logo: Optional[str] = None
    thumbnail: Optional[str] = None

    # Age Rating
    ageRangeUid: Optional[str] = None
    ageRange: Optional[str] = None

    # Program genre and completion details
    contentType: Optional[str] = None
    sgce: Optional[str] = None
    programType: Optional[str] = None
    programTypeId: Optional[int] = None
    isComplete: Optional[bool] = None
    numSeasons: Optional[int] = None

    # Team details
    director: Optional[str] = None
    producedBy: Optional[str] = None
    showMan: Optional[str] = None
    casting: Optional[str] = None
    technicalTeam: Optional[str] = None

    idWiki: Optional[str] = None

    # Foreign Keys and Relationships
    pubState_id: Optional[int] = Field(default=None, foreign_key="tvpubstate.id")
    channel_id: Optional[int] = Field(default=None, foreign_key="tvchannel.id")

    pubState: Optional[TVPubState] = Relationship()
    channel: Optional[TVChannel] = Relationship(back_populates="programs")
    genres: Optional[List[TVGenres]] = Relationship(
        back_populates="programs",
        link_model=TVProgramGenreLink,
    )

    @field_validator('publicationDate', mode="before")
    def validate_publication_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d-%m-%Y %H:%M:%S')
            except ValueError:
                raise ValueError('Invalid date format')
        return v


# ---- Refactor SQLModel

    # # Media details
    # orden = Column(Integer, nullable=True)
    # imageSEO = Column(String, nullable=True)
    # logo = Column(String, nullable=True)
    # thumbnail = Column(String, nullable=True)

    # # Age Rating
    # ageRangeUid = Column(String, nullable=True)
    # ageRange = Column(String, nullable=True)

    # # Program genre and completion details
    # contentType = Column(String, nullable=True)
    # sgce = Column(String, nullable=True)
    # programType = Column(String, nullable=True)
    # programTypeId = Column(Integer, nullable=True)
    # isComplete = Column(Boolean, nullable=True)
    # numSeasons = Column(Integer, nullable=True)

    # # Team details
    # director = Column(String, nullable=True)
    # producedBy = Column(String, nullable=True)
    # showMan = Column(String, nullable=True)
    # casting = Column(String, nullable=True)
    # technicalTeam = Column(String, nullable=True)

    # idWiki = Column(String, nullable=True)
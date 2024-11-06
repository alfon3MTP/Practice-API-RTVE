from pydantic import BaseModel
from typing import List
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import HttpUrl


class Genre(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    programs: List["Program"] = Relationship(back_populates="genre")


class Channel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    permalink: str
    html_url: HttpUrl

    programs: List["Program"] = Relationship(back_populates="channel")


class PublicationState(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    code: str
    description: str

    programs: List["Program"] = Relationship(back_populates="pub_state")


class Program(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    emission: Optional[str] = None
    publication_date: Optional[str] = None
    logo_url: Optional[HttpUrl] = None

    channel_id: int = Field(foreign_key="channel.id")
    genre_id: int = Field(foreign_key="genre.id")
    pub_state_id: int = Field(foreign_key="publicationstate.id")

    channel: Channel = Relationship(back_populates="programs")
    genre: Genre = Relationship(back_populates="programs")
    pub_state: PublicationState = Relationship(back_populates="programs")


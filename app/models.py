from pydantic import BaseModel, AnyUrl, field_validator

from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship




## Pydantic Model (This is not necessary, it's just to practice)

## RTVE API Response

class TVPubState(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    
class TVChannel(BaseModel):
    title: Optional[str] = None
    htmlUrl: Optional[AnyUrl] = None
    uid: Optional[str] = None
    
class TVGenres(BaseModel):
    generoInf: Optional[str] = None
    generoInfUid: Optional[str] = None
    generoId: Optional[str] = None

class TVProgram(BaseModel):
    # Basic info
    htmlUrl: AnyUrl
    uid: str
    name: str
    language: Optional[str] = None
    description: Optional[str] = None
    emission: Optional[str] = None
    publicationDate: Optional[datetime] = None
    
    # Media
    orden: Optional[int] = None
    imageSEO: Optional[str] = None
    logo: Optional[str] = None
    thumbnail: Optional[str] = None
    
    # Age Rating
    ageRangeUid: Optional[str] = None
    ageRange: Optional[str] = None
    
    # Program genre and completion
    contentType: Optional[str] = None
    sgce: Optional[str] = None
    programType: Optional[str] = None
    programTypeId: Optional[int] = None
    isComplete: Optional[bool] = None
    numSeasons: Optional[int] = None
    
    # Direction
    director: Optional[str] = None #"Jero Rodríguez",
    producedBy: Optional[str] = None #"Isabel Blesa | Josep Parés",
    showMan: Optional[str] = None #"Maika Makovski",
    casting: Optional[str] = None #null,
    technicalTeam: Optional[str] = None #"Xavier Lomba hay una parte | Juan Caballero | Alfredo Carracedo | Guillem Nualart",
    
    idWiki: Optional[AnyUrl] = None
    
    pubState: TVPubState
    channel: TVChannel
    generos: List[TVGenres]
    
    @field_validator('publicationDate', mode="before")
    def validate_publication_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d-%m-%Y %H:%M:%S')
            except ValueError:
                raise ValueError('Invalid date format')
        return v

class TVPage(BaseModel):
    items: List[TVProgram]



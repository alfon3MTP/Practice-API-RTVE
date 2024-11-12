# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Member(BaseModel):
    name: str
    role: str
    
    class Config:
        orm_mode = True

class Team(BaseModel):
    name: str
    description: str
    members: Optional[List[Member]] = []
    
    class Config:
        orm_mode = True

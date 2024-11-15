from pydantic import BaseModel
from typing import List, Optional

# Team Schemas
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    members: List["MemberBase"] = []  

    class Config:
        orm_mode = True


# Member Schemas
class MemberBase(BaseModel):
    name: str
    age: Optional[int] = None 
    team_id: Optional[int] = None

class MemberCreate(MemberBase):
    inventory_items: Optional[List["InventoryItemCreate"]] = []
    roles: Optional[List["RoleCreate"]] = []  
    pass

class Member(MemberBase):
    id: int
    inventory_items: List["InventoryItemBase"] = [] 
    roles: List["RoleBase"] = []

    class Config:
        orm_mode = True


# InventoryItem Schemas
class InventoryItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(InventoryItemBase):
    id: int
    member_id: int

    class Config:
        orm_mode = True


# Role Schemas
class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


# Shema response API Page

class PageInfo(BaseModel):
    number: int
    size: int
    offset: int
    total: int
    totalPages: int
    numElements: int
    items: List[dict]  # Adjust this to a specific schema if items have known structure

class APIResponse(BaseModel):
    page: PageInfo


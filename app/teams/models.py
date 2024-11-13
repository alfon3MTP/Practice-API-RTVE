from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.database import Base

# N:M Relationship
member_roles = Table(
    'member_roles', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# Tables
class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # age = Column(Integer, nullable=True)
    # alias = Column(String, nullable=True)
    description = Column(String)
    
    members = relationship("Member", back_populates="team")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    age = Column(Integer, nullable=True)
    alias = Column(String, nullable=True)
    # alias2 = Column(String, nullable=True)
    
    team = relationship("Team", back_populates="members")
    inventory_items = relationship("InventoryItem", back_populates="owner")
    roles = relationship("Role", secondary=member_roles, back_populates="members")  # Fixed here

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"))

    owner = relationship("Member", back_populates="inventory_items")
    
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Many-to-many relationship with members
    members = relationship("Member", secondary=member_roles, back_populates="roles")  # Fixed here

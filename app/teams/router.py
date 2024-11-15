from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.teams import models, schemas
import app.teams.utils as tm_utils

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


# Team Endpoints
@router.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = models.Team(name=team.name, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/teams/{team_id}", response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Member Endpoints
@router.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    # Create the Member
    db_member = models.Member(name=member.name, team_id=member.team_id)
    db.add(db_member)
    db.commit()  # Commit the member first to get its ID

    if member.inventory_items:
        for item in member.inventory_items:
            db_item = models.InventoryItem(name=item.name, description=item.description, member_id=db_member.id)
            db.add(db_item)

    if member.roles:
        for role in member.roles:
            
            db_role = tm_utils.get_or_create_role(db, role.name)
            db_member.roles.append(db_role)

    db.commit()  
    db.refresh(db_member) 

    return db_member


@router.get("/members/{member_id}", response_model=schemas.Member)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# Inventory Item Endpoints
@router.post("/inventory_items/", response_model=schemas.InventoryItem)
def create_inventory_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    db_item = models.InventoryItem(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/inventory_items/{item_id}", response_model=schemas.InventoryItem)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Role Endpoints
@router.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):

    db_role = tm_utils.get_or_create_role(db, role.name)

    return db_role

@router.get("/roles/{role_id}", response_model=schemas.Role)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

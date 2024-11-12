from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.teams.shema import Team as TeamSchema, Member as MemberSchema
from app.teams.models import Team, Member
from app.database.database import get_db

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.get("/", response_model=list[TeamSchema])
def get_teams(db: Session = Depends(get_db)):
    """Fetch all teams."""
    return db.query(Team).all()

@router.post("/", response_model=TeamSchema)
def create_team(team: TeamSchema, db: Session = Depends(get_db)):
    """Create a new team."""
    existing_team = db.query(Team).filter(Team.name == team.name).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team already exists")

    new_team = Team(name=team.name, description=team.description)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    for member_data in team.members:
        new_member = Member(name=member_data.name, role=member_data.role, team_id=new_team.id)
        db.add(new_member)
    db.commit()

    return new_team

@router.post("/init", response_model=dict)
def initialize_mock_data(db: Session = Depends(get_db)):
    """Initialize the database with mock data."""
    sample_teams = [
        Team(name="Team Alpha", description="An elite team of experts."),
        Team(name="Team Beta", description="Special ops team.")
    ]
    db.add_all(sample_teams)
    db.commit()

    members = [
        Member(name="Alice", role="Leader", team_id=sample_teams[0].id),
        Member(name="Jose", role="Technician", team_id=sample_teams[0].id),
        Member(name="Bob", role="Manager", team_id=sample_teams[1].id),
        Member(name="Carol", role="Programmer", team_id=sample_teams[1].id)
    ]
    db.add_all(members)
    db.commit()

    return {"message": "Mock data initialized"}

import random

from app.rtve.schemas import ProgramTypeEnum, ProgramAge
from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Annotated
from sqlmodel import select, func, Session
from app.rtve.models import TVProgram

from app.db import get_session



router = APIRouter(
    prefix="/rtve",
    tags=["RTVE API"]
)

@router.get("/ping", summary="API Connectivity Test")
def ping_rtve():
    #Docstring
    """Quickly test API connectivity without significant load on the system."""
    return {"message": "Welcome to RTVE Router"}

@router.get('/program/{program_id}', summary="Get TV Program by ID")
async def get_program(
    program_id: Annotated[int, Path(title="Program ID")],
    session: Session = Depends(get_session)
) -> TVProgram:
    """Fetch a TV program by its ID from the RTVE API."""
    
    program = session.get(TVProgram, program_id)
    
    print(program)
    
    if program is None:
        raise HTTPException(status_code=404, detail='Program not found')
    return program

@router.get('/random_program', summary="Get a random TV Program")
async def get_random_program(
    session: Session = Depends(get_session)
) -> TVProgram:
    """Fetch a random TV program"""
    
    num_progrms = session.exec(
        select(
            func.count()
        ).select_from(TVProgram)
    )
    
    rand_id = random.randint(1, num_progrms.one())
    
    program = session.get(TVProgram, rand_id)
    
    if program is None:
        raise HTTPException(status_code=404, detail='Program not found')
    return program


@router.get("/random_program_type", summary="Get a Random Program by Type")
async def get_random_program_type(
    program_type: ProgramTypeEnum = None,
    age_range: ProgramAge = None,
    session: Session = Depends(get_session)
):

    query = select(TVProgram)
    
    if program_type:
        query = query.where(TVProgram.programType == program_type)
    
    print(age_range)
    if age_range:
        query = query.where(TVProgram.ageRangeUid == age_range)
        
    result = session.exec(query).all()
    
    if not result:
        raise HTTPException(status_code=404, detail="No programs found")
    
    random_program = random.choice(result)
    
    return random_program


@router.get("/program_by_showman", summary="Find Program by Showman")
async def find_program_by_showman(
    showman: str, 
    session: Session = Depends(get_session)
):
    result = session.exec(
        select(TVProgram).where(TVProgram.showMan.ilike(f"%{showman}%"))
    ).all()

    if not result:
        raise HTTPException(status_code=404, detail="No programs found for the given showman")

    return result

@router.get("/program_by_name", summary="Find Program by Name")
async def find_program_by_name(
    name: str, 
    session: Session = Depends(get_session)
):
    result = session.exec(
        select(TVProgram).where(TVProgram.name.ilike(f"%{name}%"))
    ).all()

    if not result:
        raise HTTPException(status_code=404, detail="No programs found with the given name")

    return result
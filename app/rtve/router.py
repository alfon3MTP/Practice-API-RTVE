import random

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
    
    print(num_progrms)
    
    rand_id = random.randint(1, 4668)
    
    program = session.get(TVProgram, rand_id)
    
    if program is None:
        raise HTTPException(status_code=404, detail='Program not found')
    return program
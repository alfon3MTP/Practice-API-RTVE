import random

from fastapi import APIRouter, HTTPException, Path, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.rtve import models, schemas
from app.database.database import get_db

router = APIRouter(
    prefix="/rtve",
    tags=["RTVE API"]
)


@router.get("/ping", summary="API Connectivity Test")
def ping_rtve():
    """Quickly test API connectivity without significant load on the system."""
    return {"message": "Welcome to RTVE Router"}

@router.get('/program/{program_id}', summary="Get TV Program by ID")
async def get_program(
    program_id: Annotated[int, Path(title="Program ID")],
    db: Session = Depends(get_db)
) -> schemas.Program: 
    """Fetch a TV program by its ID from the RTVE API."""
    
    program = db.query(models.Program).filter(models.Program.id == program_id).first()
    
    if program is None:
        raise HTTPException(status_code=404, detail='Program not found')

    return program


@router.get("/available_genres", summary="Get All Available Genres")
async def get_available_genres(
    db: Session = Depends(get_db)
):
    """Fetch all unique genres available in the database."""
    genres = db.query(models.Genre).all()

    if not genres:
        raise HTTPException(status_code=404, detail="No genres found")

    return [{"id": genre.id, "name": genre.generoInf} for genre in genres]

@router.get("/random_program/{genre}", summary="Get a Random Program by Genre")
async def get_random_program(
    genre: schemas.GenreEnum = Path(title="Genre from the Enum"),
    db: Session = Depends(get_db)
):
    """Fetch a random program for the selected genre."""
    
    genre_record = db.query(models.Genre).filter(models.Genre.generoInf == genre.value).first()

    if not genre_record:
        raise HTTPException(status_code=404, detail=f"Genre '{genre.value}' not found")

    genre_id = genre_record.id

    programs = db.query(models.Program).join(models.program_genre).filter(models.program_genre.c.genre_id == genre_id).all()


    if not programs:
        raise HTTPException(status_code=404, detail=f"No programs found for the genre: {genre.value}")

    return random.choice(programs)
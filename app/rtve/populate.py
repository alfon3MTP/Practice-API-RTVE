import requests

from app.rtve import models, schemas
from sqlalchemy.orm import Session
from sqlmodel import select

from app.database.database import get_db


RTVE_API_URL = "https://www.rtve.es/api/"
MAX_PAGE_SIZE = 60 



# Save Channel
def save_channel(db: Session, channel_data: schemas.ChannelBase) -> models.Channel:
    db_channel = db.query(models.Channel).filter(models.Channel.uid == channel_data.uid).first()
    
    if not db_channel:
        db_channel = models.Channel(**channel_data.model_dump())
        db.add(db_channel)
        db.commit()
        db.refresh(db_channel)
    
    return db_channel

# Save PubState
def save_pub_state(db: Session, pub_state_data: schemas.PubStateBase) -> models.PubState:
    db_pub_state = db.query(models.PubState).filter(models.PubState.code == pub_state_data.code).first()
    if not db_pub_state:
        db_pub_state = models.PubState(**pub_state_data.model_dump())
        db.add(db_pub_state)
        db.commit()
        db.refresh(db_pub_state)
    return db_pub_state

# Save Genre
def save_genre(db: Session, genre_data: schemas.GenreBase) -> models.Genre:
    db_genre = db.query(models.Genre).filter(models.Genre.generoId == genre_data.generoId).first()
    if not db_genre:
        db_genre = models.Genre(**genre_data.model_dump())
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
    return db_genre

# Save Program
def save_program(db: Session, program_data: schemas.ProgramCreate) -> models.Program:
    db_channel = save_channel(db, program_data.channel) if program_data.channel else None
    db_pub_state = save_pub_state(db, program_data.pubState) if program_data.pubState else None
    
    print(program_data.generos)
    
    db_genres = [save_genre(db, genre) for genre in program_data.generos] if program_data.generos else []
    
    db_program = db.query(models.Program).filter(models.Program.uid == program_data.uid).first()
    if not db_program:
        db_program = models.Program(**program_data.model_dump(exclude={"channel", "pubState", "generos", "id"}))
        db_program.channel = db_channel
        db_program.pubState = db_pub_state
        db_program.generos = db_genres
        
        db.add(db_program)
        db.commit()
        db.refresh(db_program)
    
    return db_program

#https://www.rtve.es/api/programas.json?size=60&page=2
def fetch_programs(size: int, page: int) -> schemas.APIResponse:
    endpoint = "programas.json"
    url_filters = f"?size={size}&page={page}"
    url = f"{RTVE_API_URL}{endpoint}{url_filters}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    api_response = schemas.APIResponse(**data)
    
    return api_response

def save_items():
    db = next(get_db())
    api_response = fetch_programs(MAX_PAGE_SIZE, 1)
    page = api_response.page
    
    while page.number < page.totalPages:
        
        for program_data in page.items:
            save_program(db, program_data)
            
        
        # if page.number > 2:
        #     exit()
        
        api_response = fetch_programs(MAX_PAGE_SIZE, page.number + 1)
        page = api_response.page
        

def delete_all_data():
    db = next(get_db())
    try:
        # Deleting rows from all tables
        db.query(models.Program).delete()
        db.query(models.Genre).delete()
        db.query(models.PubState).delete()
        db.query(models.Channel).delete()
        db.query(models.program_genre).delete()
        
        db.commit()
    finally:
        db.close()


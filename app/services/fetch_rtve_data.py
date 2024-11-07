import requests
from app.models import * 

from sqlalchemy.orm import Session
from sqlmodel import select


RTVE_API_URL = "https://www.rtve.es/api/"
MAX_PAGE_SIZE = 60 


def parse_datetime(date_str: str) -> Optional[datetime]:
    """Helper function to parse date from the API format."""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        return None

#https://www.rtve.es/api/programas.json?size=60&?page=2
def fetch_programs(size: int, page: int, engine):
    endpoint = "programas.json"
    url_filters = f"?size={size}&page={page}"
    url = f"{RTVE_API_URL}{endpoint}{url_filters}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    programs_data = data.get("page", {}).get("items", [])
    
    with Session(engine) as session:
        programs_to_add = []

        for program_data in programs_data:
            # Check for existing program based on unique identifier (e.g., uid or htmlUrl)
            existing_program = session.execute(select(TVProgram).filter(TVProgram.uid == program_data["uid"])).scalar_one_or_none()
            if existing_program:
                print(f"Skipping existing program: {program_data['name']} with uid: {program_data['uid']}")
            else:
                # Check and create the pubState if it doesn't exist
                pub_state_data = program_data.get("pubState", {})
                pub_state = session.execute(select(TVPubState).filter(TVPubState.code == pub_state_data.get("code"))).scalar_one_or_none()
                if not pub_state and pub_state_data:
                    pub_state = TVPubState(**pub_state_data)
                    session.add(pub_state)

                # Check and create the channel if it doesn't exist
                channel_data = program_data.get("channel", {})
                channel = session.execute(select(TVChannel).filter(TVChannel.uid == channel_data.get("uid"))).scalar_one_or_none()
                if not channel and channel_data:
                    channel = TVChannel(**channel_data)
                    session.add(channel)

                # Check and create genres dynamically
                
                # Convert program data into TVProgram instance
                program = TVProgram(
                    htmlUrl=program_data["htmlUrl"],
                    uid=program_data["uid"],
                    name=program_data["name"],
                    language=program_data.get("language"),
                    description=program_data.get("description"),
                    emission=program_data.get("emission"),
                    publicationDate=parse_datetime(program_data.get("publicationDate")),
                    orden=program_data.get("orden"),
                    imageSEO=program_data.get("imageSEO"),
                    logo=program_data.get("logo"),
                    thumbnail=program_data.get("thumbnail"),
                    ageRangeUid=program_data.get("ageRangeUid"),
                    ageRange=program_data.get("ageRange"),
                    contentType=program_data.get("contentType"),
                    sgce=program_data.get("sgce"),
                    programType=program_data.get("programType"),
                    programTypeId=program_data.get("programTypeId"),
                    isComplete=program_data.get("isComplete"),
                    numSeasons=program_data.get("numSeasons"),
                    director=program_data.get("director"),
                    producedBy=program_data.get("producedBy"),
                    showMan=program_data.get("showMan"),
                    casting=program_data.get("casting"),
                    technicalTeam=program_data.get("technicalTeam"),
                    idWiki=program_data.get("idWiki"),
                    pubState_id=pub_state.id if pub_state else None,
                    channel_id=channel.id if channel else None,
                )

                genres_data = program_data.get("generos", [])
                if genres_data is None:
                    genres_data = []
                
                genre_objects = []
                for genre_data in genres_data:
                    genre = session.execute(select(TVGenres).filter(TVGenres.generoId == genre_data.get("generoId"))).scalar_one_or_none()
                    if not genre and genre_data:
                        genre = TVGenres(**genre_data)
                        session.add(genre)

                    # Check if the program already has this genre
                    if program:
                        existing_link = session.execute(
                            select(TVProgramGenreLink).filter(
                                TVProgramGenreLink.program_id == program.id,
                                TVProgramGenreLink.genre_id == genre.id
                            )
                        ).scalar_one_or_none()

                        # If the link doesn't exist, add it to the list of genre objects
                        if not existing_link:
                            genre_objects.append(genre)

                # Add the genres relationship
                program.genres = genre_objects
                programs_to_add.append(program)

        # Commit the session after processing all programs
        session.add_all(programs_to_add)
        session.commit()
        print(f"Inserted {len(programs_to_add)} new programs into the database.")
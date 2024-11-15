from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pydantic import field_validator

class ProgramTypeEnum(str, Enum):
    serie_documental = "Serie Documental"
    infantiles = "Infantiles"
    documental_original = "Documental Original"
    magacines = "Magacines"
    entrevistas = "Entrevistas"
    magacin_semanal = "Magacín semanal"
    informativos_noticias = "Informativos Noticias"
    entretenimiento = "Entretenimiento"
    concursos = "Concursos"
    reportajes_factual = "Reportajes Factual"
    series_ficcion_originales = "Series Ficción Originales"
    magacines_diarios = "Magacines diarios"
    talent = "Talent"
    conciertos = "Conciertos"
    series_internacionales = "Series Internacionales"
    series = "Series"
    series_prime_time = "Series Prime Time"
    late_night = "Late Night"
    especial_evento = "Especial Evento"
    series_archivo = "Series de Archivo"
    series_diarias = "Series Diarias"
    recetas = "Recetas"
    documental = "Documental"
    series_catalan = "Series catalán"
    contenedor_peliculas = "Contenedor Películas"
    informativo_diario = "Informativo diario"
    entretenimiento_no_usar = "Entretenimiento NO USAR"
    
class ProgramAge(str, Enum):
    
    IF_REDAD0 = 'Recomendado para todos los públicos'
    IF_REDAD2 = 'Recomendado para mayores de 7 años'
    IF_REDAD5 = 'Recomendado para mayores de 12 años'
    IF_REDAD3 = 'Recomendado para mayores de 13 años'
    IF_REDAD6 = 'Recomendado para mayores de 16 años'
    IF_REDAD4 = 'Recomendado para mayores de 18 años'
    IF_REDAD1 = 'Especialmente recomendado para la infancia'

class GenreEnum(Enum):
    VIAJES = "Viajes"
    ARCHIVO_TVE = "Archivo TVE"
    BIOGRAFIAS = "Biografías"
    INFANTIL = "Infantil"
    COCINA = "Cocina"
    CULTURA = "Cultura"
    CIENCIA_Y_FUTURO = "Ciencia y futuro"
    INFORMACION_Y_ACTUALIDAD = "Información y actualidad"
    HISTORIA = "Historia"
    POLICIACA_Y_SUSPENSE = "Policíaca y suspense"
    MUSICA = "Música"
    SERVICIO_PUBLICO = "Servicio Público"
    DRAMA = "Drama"
    SERIES = "Series"
    DEPORTES = "Deportes"
    PLAYZ_JOVEN = "Playz joven"
    HUMOR = "Humor"
    MODA_FAMOSOS_Y_TENDENCIAS = "Moda, famosos y tendencias"
    TERROR = "Terror"
    SERIES_LITERARIAS = "Series Literarias"
    CATALUNA = "Cataluña"
    SERIES_HISTORICAS = "Series Históricas"
    IGUALDAD = "Igualdad"
    ACCION_Y_AVENTURAS = "Acción y aventuras"
    COMEDIA = "Comedia"
    TV_MOVIES = "TV Movies"
    ROMANTICA = "Romántica"
    SOBREMESA = "Sobremesa"
    SERIES_EN_CATALAN = "Series en Catalán"

# PubState SHCEMAS
class PubStateBase(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    
class PubStateCreate(PubStateBase):
    pass

class PubState(PubStateBase):
    id: int

    class Config:
        from_attributes = True

# Channel SHCEMAS
class ChannelBase(BaseModel):
    title: Optional[str] = None
    htmlUrl: Optional[str] = None
    uid: Optional[str] = None
    
class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    id: int
    programs: List["Program"] = []  # List of associated programs

    class Config:
        from_attributes = True

# Genre SHCEMAS
class GenreBase(BaseModel):
    generoInf: Optional[str] = None
    generoInfUid: Optional[str] = None
    generoId: Optional[str] = None
    
class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    programs: List["Program"] = []
    class Config:
        from_attributes = True

# Program SHCEMAS
class ProgramBase(BaseModel):
    htmlUrl: Optional[str] = None
    uid: Optional[str] = None
    name: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    emission: Optional[str] = None
    publicationDate: Optional[datetime] = None
    channel_id: Optional[int] = None
    pub_state_id: Optional[int] = None
    
    director: Optional[str]
    producedBy: Optional[str]
    showMan: Optional[str]
    
    ageRangeUid: Optional[str]
    ageRange: Optional[str]
    
    
    
    @field_validator('publicationDate', mode="before")
    def validate_publication_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d-%m-%Y %H:%M:%S')
            except ValueError:
                raise ValueError('Invalid date format')
        return v
    
class ProgramCreate(ProgramBase):
    generos: Optional[List[GenreBase]] = []
    channel: Optional[ChannelBase] = None
    pubState: Optional[PubStateBase] = None
    
class Program(ProgramBase):
    id: int
    channel: Optional[ChannelBase] = None
    pubState: Optional[PubStateBase] = None
    generos: Optional[List[GenreBase]] = []
    class Config:
        from_attributes = True

# Shema response API Page

class PageInfo(BaseModel):
    number: int
    size: int
    offset: int
    total: int
    totalPages: int
    numElements: int
    items: List[Program]

class APIResponse(BaseModel):
    page: PageInfo


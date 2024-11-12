from enum import Enum
from pydantic import BaseModel

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
    

class ProgarmQuery(BaseModel):
    name: str
    
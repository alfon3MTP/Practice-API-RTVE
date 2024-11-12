### Prueba de stack

* Fast API: Routers
* pydantic
* Alembic
* SQLite + SQLModels (un wraper de SQL Alchemy)
* Tests: Integración, unitarios y cobertura
* ETL (Extracción Transformación y Carga, de manera ligera y opcional)


La intencionalidad es crear y poblar una base de datos sobre la cual se realizarán consultas mediante FastAPI

APIs usadas: 

https://es.wikibooks.org/wiki/API_Rtve
https://github.com/UlisesGascon/RTVE-API



Tres formatos diferentes:

* RTVE: Sus modelos y base de datos están hecho susando SQLModels
    * Problema: Las relaciones no se reflejan en las consultas, no hay Shema

* Monitoring: Ejemplo de creación de un router, sin base de datos implementada

* Teams: Con base de datos integrada y relación, shema y moedelos separados, integracón con Alembic
    * The place to be 


Commands: 

Usar `python 3.11.8` (Última versión security)

```cmd

venv install -r requirements.txt

alembic init alembic
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

run main.py
```
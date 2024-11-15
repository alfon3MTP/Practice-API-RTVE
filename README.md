### Prueba de stack

Tecnologías a utilizar

* Fast API: Routers
* pydantic
* Alembic
* ETL con Pydantic
* SQLModels: (Probado pero no continuado)
* Tests: TODO

## Documentación:

* Carpeta /docs
  * Alembic
  * FastAPI Models

Documentación APIs usadas:

[https://es.wikibooks.org/wiki/API_Rtve]()
[https://github.com/UlisesGascon/RTVE-API]()

Tres formatos diferentes:

* RTVE: Sus modelos y base de datos están hecho susando SQLModels

  * Problema: Las relaciones no se reflejan en las consultas, no hay Shema
* Monitoring: Ejemplo de creación de un router, sin base de datos implementada
* Teams: Con base de datos integrada y relación, shema y moedelos separados, integracón con Alembic

  * El estándar

Commands:

Usar `python 3.11.8` (Última versión security)

```cmd

venv install -r requirements.txt
run main.py
```

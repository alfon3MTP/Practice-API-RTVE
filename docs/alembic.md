Configuración Alembic 


    1. Estructura de Migraciones

Para empezar se debe crear la estructura de migraciones con el siguiente comando
alembic init migrations

O si prefieres otro nombre para la carpeta de migraciones, puedes usar:
alembic init alembic

Esto generará la carpeta migrations (o el nombre que elijas), que contendrá los archivos env.py y script.py.mako. Además, fuera de esta carpeta se generará el archivo alembic.ini.

    2. Archivo alembic.ini

Este archivo con la configuración básica para conectar Alembic con la base de datos. 

[alembic]
# Ruta a los scripts de migración
script_location = alembic

# Configuración de la URL de la base de datos (SQLite en este caso)
sqlalchemy.url = sqlite:///database.db



    3. Configuración del archivo env.py

En este archivo se configura el entorno de ejecución de las migraciones. Es importante importar todos los modelos de la base de datos aquí. De esta manera Alembic puede detectar las tablas y sus cambios.


# Importar modelos para la base de datos
from app.teams.models import *

# Seleccionar ubicación de la base de datos
config.set_main_option('sqlalchemy.url', f"sqlite:///database.db")

# Asigna la metadata de tu base de datos
target_metadata = Base.metadata

Una vez configurado, podremos crear la primera migración (siempre que existan los modelos)

    4. Crear y Aplicar Migraciones

alembic revision --autogenerate -m "Initial Tables"

Y para aplicar los cambios se debe ejecutar 

alembic upgrade head

Según añadamos más modelos, columnas y cambios, se podrán crear nuevas versiones.

alembic revision --autogenerate -m "Column age added to Member"

Nuevamente hay que aplicar la migración

alembic upgrade head

Exsiten extensiones para vs code para ver el contenido de la base de datos, en este caso he utilizado "sqlite3 editor" para ver cómo se iban aplicando los cambios a la base de datos. 

    5. Comandos adicionales

retroceder a una versión específica o anterior
alembic downgrade <revision_id>
alembic downgrade -1

versión actual
alembic current

listar el historial completo de migraciones
alembic history --verbose
## Configuración Alembic 

### 1. Estructura de Migraciones

Para empezar se debe crear la estructura de migraciones con el siguiente comando

``` 
alembic init migrations
```

O si se prefiere usar otro nombre para la carpeta de migraciones, puedes usar
```
alembic init *nombre_carpeta_migraciones*
```

Esto generará la carpeta migrations (_o el nombre que elijas_), que contendrá los archivos ``env.py`` y ``script.py.mako``. Además, fuera de esta carpeta se generará el archivo ``alembic.ini``.

### 2. Archivo alembic.ini

Este archivo con la configuración básica para conectar Alembic con la base de datos. 
````
[alembic]
# Ruta a los scripts de migración
script_location = alembic

# Configuración de la URL de la base de datos (SQLite en este caso)
sqlalchemy.url = sqlite:///database.db
````

### 3. Configuración del archivo env.py

En este archivo se configura el entorno de ejecución de las migraciones. Es importante importar todos los modelos de la base de datos aquí. De esta manera Alembic puede detectar las tablas y sus cambios.

````
# Importar modelos para la base de datos
from app.teams.models import *

# Seleccionar ubicación de la base de datos
config.set_main_option('sqlalchemy.url', f"sqlite:///database.db")

# Asigna la metadata de tu base de datos
target_metadata = Base.metadata
````
Una vez configurado, podremos crear la primera migración (siempre que existan los modelos)

### 4. Crear y Aplicar Migraciones

Para crear una nueva migración, o más bien si no hy crear la primera. Lanzar el comando: 

```
alembic revision --autogenerate -m "Initial Tables"
```
Esto creará un nuevo script de migracioness en la carpeta ``versions``, aunque si nos fijamos en la BBDD, esta aún no habrá contemplado los cambios. Para reflejarlos, se debe lanzar: 
```
alembic upgrade head
```
El cual aplica los cambios más recientes ``head``, aunque si queremos ir a cualquier otro punto del versionado se puede poner el identificador de la versión. 


Asimismo, según añadamos más modelos, columnas y cambios, se podrán crear nuevas versiones.

```
alembic revision --autogenerate -m "Column age added to Member"
```
Nuevamente hay que aplicar la migración

alembic upgrade head

Exsiten extensiones para vs code para ver el contenido de la base de datos, en este caso he utilizado "sqlite3 editor" para ver cómo se iban aplicando los cambios a la base de datos. 

### 5. Comandos adicionales

Retroceder a una versión específica o anterior
```
alembic downgrade <revision_id>
alembic downgrade -1
```
Versión actual
```
alembic current
```

Listar el historial completo de migraciones

```
alembic history --verbose
```
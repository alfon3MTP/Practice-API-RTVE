Ya existe una documentación muy extensa de FastAPI con ejemplos.

Tutoriales:

[Curso FastAPI](https://youtube.com/playlist?list=PL-2EBeDYMIbQghmnb865lpdmYyWU3I5F1&si=xhSn5_Ld4vUueg4R)

[https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-1-of-4-1113515037fd
](https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-1-of-4-1113515037fd)[https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-2-of-4-2bca8a10e7f1
](https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-2-of-4-2bca8a10e7f1)[https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-3-of-4-702698ec5a10
](https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-3-of-4-702698ec5a10)[https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-4-of-4-c6928c8fd37b](https://levelup.gitconnected.com/best-practices-for-modern-rest-apis-in-python-part-4-of-4-c6928c8fd37b)

Best Practices

[https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file](https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file)

[fastapi_best_architecture/backend at master · fastapi-practices/fastapi_best_architecture](https://github.com/fastapi-practices/fastapi_best_architecture/tree/master/backend)

[https://github.com/fastapi-practices]()

Estructura general:

La que por ahora he probado me resulta la más limpia en el caso que los modelos sean muchos y puedan dividirse.
Asimismo, cada sección contará con `models`, `router` y `shemas`. Asimismo, si el proyecto requiriese otra estructura más simplificada, para las etapas iniciales también se debe valorar, antes de empezar a crear carpetas de más dificultando el desarrollo. 

**`models.py`** : Define las clases que representan las tablas en la base de datos. Usando SQLAlchemy, y representan las entidades de la aplicación (por ejemplo, `Member`, `Team` o `role`). Cada clase refleja la estructura de una tabla en la base de datos.

Ejemplo:

```python
# teams/models.py
class Team(Base):
    __tablename__ = "teams"
  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
  
    members = relationship("Member", back_populates="team")

class Member(Base):
    __tablename__ = "members"
  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    age = Column(Integer, nullable=True)
    alias = Column(String, nullable=True)
  
    team = relationship("Team", back_populates="members")
```

Para Realciones Many to Many

```python

member_roles = Table(
    'member_roles', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Many-to-many relationship with members
    members = relationship("Member", secondary=member_roles, back_populates="roles")


```

`shema.py`

Define las estructuras de datos para las operaciones de entrada y salida (requests/responses) que usa la API mdeiante Pydantic.

Diferenciando Base, Create, Model


1. Base
   Es el esquema "base" que contiene los atributos principales de un modelo. Sin sus relaciones con otros modelos.
2. Create
   Extiende de base e incluye detalles adicionales para el modelo. Como otros modelos que se deben crear a partir de éste.
3. Member:
   También extiende de member base, y es el que el usuario recibirá de vuelta en la llamada. Pudiendo así limitar los campos que se quiran enviar.
   1. `orm = True`, se utiliza para automáticamente convertir la información del modelo de base de datos a este esquema cuando se devuelva al l cliente

Como sep uede ver cada shema tiene su propia función, se entiende mejor al implementarlo en una vista/enpont. 


```python
class MemberBase(BaseModel):
    name: str
    age: Optional[int] = None 
    team_id: Optional[int] = None

class MemberCreate(MemberBase):
    inventory_items: Optional[List["InventoryItemCreate"]] = []
    roles: Optional[List["RoleCreate"]] = []  
    pass

class Member(MemberBase):
    id: int
    inventory_items: List["InventoryItemBase"] = [] 
    roles: List["RoleBase"] = []

    class Config:
        orm_mode = True
```


Enpoint 

Según la naturaleza del enpoint devolveremos un schema u otro, en este caso, será el de un miembro. Y como s epretende crear uno, recibirá como parámetro de entrada un Member Create, que podrá contener asímismo información acerca de su inventario y rol. No obstante, el shema únicamente comprobará que el tipo de dato corresponde con el del modelo. Una vez comprobados los valores, mediante pydantic se podrá guardar en la base de datos. 


TODO: Añadir excepciones en caso de error. 

En este caso podría haber una serie de fallos que podrían darse y sería conveniente notificar en la respuesta:

* Rol ya existente
* Datos del miembro que faltan y son obligatorios
* Fallos en el tipo (ej. poner en el campo de edad un string)
* Campos incorrectos

Crear una categoría de fallos unificada  

```python
from app.teams import models, schema

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.post("/members/", response_model=schema.Member)
def create_member(member: schema.MemberCreate, db: Session = Depends(get_db)):
    # Create the Member
    db_member = models.Member(name=member.name, team_id=member.team_id)
    db.add(db_member)
    db.commit()  # Commit the member first to get its ID

    if member.inventory_items:
        for item in member.inventory_items:
            db_item = models.InventoryItem(name=item.name, description=item.description, member_id=db_member.id)
            db.add(db_item)

    if member.roles:
        for role in member.roles:
  
            db_role = tm_utils.get_or_create_role(db, role.name)
            db_member.roles.append(db_role)

    db.commit()  
    db.refresh(db_member) 

    return db_member
```



```
C:.
│   .gitignore
│   alembic.ini
│   database.db
│   db.sqlite
│   main.py
│   README.md
│   requirements.txt
│   
├───app
│   │   db.py
│   │
│   ├───teams
│   │   │   models.py #
│   │   │   router.py #Módulo de FastAPI para esteconjunto de modelos
│   │   │   schema.py #Esquemas de Pydantic para FastAPI
│   │   │   utils.py  #Funciones adicionales para tratar lso datos
│   │   └──
│   ├───monitoring
│   │   │   router.py
│   │   └─
│   ├───rtve
│   │   │   fetch_rtve_data.py
│   │   │   models.py
│   │   │   router.py
│   │   │   schemas.py
│   │   └─
│   │
│   ├───database
│   │   │   database.py
│   │   │
│   │   ├───data_example
│   │   │       programs.json
│   │   │       program_group.json
│   │   └
│
├───docs
│       alembic.md
│       fastapi.md
│       TODOS.md
│
├───alembic
│   │   env.py # Todos los modelos deben estar incluidos en este .p para estar monitorizados
│   │   README
│   │   script.py.mako
│   │
│   ├───versions
│   │   │   1fb14291d432_member_alias_added.py
│   │   │   454926c36f0d_age_added.py
│   │   │   6ab37e284c8d_age_added.py
│   │   │   75e5a8c92c4d_inital_commit.py
│   │   └──
```

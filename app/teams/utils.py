from sqlalchemy.orm import Session
from app.teams import models

def get_or_create_role(db: Session, role_name: str) -> models.Role:

    existing_role = db.query(models.Role).filter(models.Role.name == role_name).first()

    if existing_role:
        return existing_role
    else:
        db_role = models.Role(name=role_name)
        db.add(db_role)
        db.commit()
        db.refresh(db_role) 
        return db_role

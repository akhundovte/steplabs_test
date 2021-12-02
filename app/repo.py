from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas
from .timezone import now


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    now_at = now()
    db_user = models.User(
        email=user.email,
        password=user.password,
        name=user.name,
        surname=user.surname,
        patronymic=user.patronymic,
        created_at=now_at,
        updated_at=now_at,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users_by_query(db: Session, query: str, offset: int = 0, limit: int = 100):
    search = f"{query}%"
    users = db.query(models.User).filter(or_(
        models.User.name.like(search),
        models.User.surname.like(search),
        models.User.patronymic.like(search)
        )).offset(offset).limit(limit).all()
    return users


def update_user(db: Session, db_user: models.User, user: schemas.UserCreate):
    is_updated = False
    for field_name, value in user:
        if getattr(db_user, field_name) != value:
            setattr(db_user, field_name, value)
            if not is_updated:
                is_updated = True

    if is_updated:
        db_user.updated_at = now()
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

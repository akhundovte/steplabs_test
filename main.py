from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from db.engine import get_session
from app import schemas, repo


app = FastAPI()


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = repo.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


@app.get("/users/", response_model=List[schemas.User])
def read_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return repo.get_users(db, offset=offset, limit=limit)


@app.get("/users/search/", response_model=List[schemas.User])
def search_users(query: str, offset: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return repo.get_users_by_query(db, query, offset, limit)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_user = repo.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Пользователь с указанной почтой уже зарегистрирован")
    return repo.create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_session)):
    db_user = repo.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return repo.update_user(db, db_user, user)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    db_user = repo.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    repo.delete_user(db, user_id)

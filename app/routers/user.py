from typing import List
from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.schemas import CreateUser, UserOut
from app.utils import hash

router = APIRouter(
    prefix="/users",
    tags=["Users",]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    is_user = db.query(models.User).filter(
        models.User.email == str(user.email)).first()
    if is_user:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user

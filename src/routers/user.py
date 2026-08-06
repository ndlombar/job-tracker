import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.dependencies import get_current_user, get_db
from src.models import User
from src.schemas import UserCreate, UserRead, UserUpdate
from src.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


def _get(db: Session, user_id: uuid.UUID) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from exc
    db.refresh(user)
    return user


@router.get("", response_model=list[UserRead], dependencies=[Depends(get_current_user)])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return list(db.execute(select(User)).scalars().all())


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_user)])
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> User:
    return _get(db, user_id)


@router.patch("/{user_id}", response_model=UserRead, dependencies=[Depends(get_current_user)])
def update_user(user_id: uuid.UUID, payload: UserUpdate, db: Session = Depends(get_db)) -> User:
    user = _get(db, user_id)
    data = payload.model_dump(exclude_unset=True)
    password = data.pop("password", None)
    if password is not None:
        user.hashed_password = hash_password(password)
    for field, value in data.items():
        setattr(user, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered") from exc
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    user = _get(db, user_id)
    db.delete(user)
    db.commit()

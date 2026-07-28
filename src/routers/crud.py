import uuid
from enum import Enum
from typing import TypeVar, cast

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


def make_crud_router(
    *,
    model: type[ModelT],
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    read_schema: type[BaseModel],
    prefix: str,
    tags: list[str | Enum],
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    def get(db: Session, item_id: uuid.UUID) -> ModelT:
        item = db.get(model, item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
        return item

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create(payload: create_schema, db: Session = Depends(get_db)) -> ModelT:  # type: ignore[valid-type]
        item = model(**cast(BaseModel, payload).model_dump())
        db.add(item)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflicting or invalid reference") from exc
        db.refresh(item)
        return item

    @router.get("", response_model=list[read_schema])  # type: ignore[valid-type]
    def list_items(db: Session = Depends(get_db)) -> list[ModelT]:
        return list(db.execute(select(model)).scalars().all())

    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: uuid.UUID, db: Session = Depends(get_db)) -> ModelT:
        return get(db, item_id)

    @router.patch("/{item_id}", response_model=read_schema)
    def update_item(item_id: uuid.UUID, payload: update_schema, db: Session = Depends(get_db)) -> ModelT:  # type: ignore[valid-type]
        item = get(db, item_id)
        for field, value in cast(BaseModel, payload).model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflicting or invalid reference") from exc
        db.refresh(item)
        return item

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
        item = get(db, item_id)
        db.delete(item)
        db.commit()

    return router

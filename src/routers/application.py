import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.models import Application
from src.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)) -> Application:
    application = Application(**payload.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=list[ApplicationRead])
def list_applications(db: Session = Depends(get_db)) -> list[Application]:
    return list(db.execute(select(Application)).scalars().all())


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: uuid.UUID, db: Session = Depends(get_db)) -> Application:
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: uuid.UUID, payload: ApplicationUpdate, db: Session = Depends(get_db)
) -> Application:
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    db.delete(application)
    db.commit()

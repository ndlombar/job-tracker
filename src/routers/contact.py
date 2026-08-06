from fastapi import Depends

from src.dependencies import get_current_user
from src.models import Contact
from src.routers.crud import make_crud_router
from src.schemas import ContactCreate, ContactRead, ContactUpdate

router = make_crud_router(
    model=Contact,
    create_schema=ContactCreate,
    update_schema=ContactUpdate,
    read_schema=ContactRead,
    prefix="/contacts",
    tags=["contacts"],
    dependencies=[Depends(get_current_user)],
)

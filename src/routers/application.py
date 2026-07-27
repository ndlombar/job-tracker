from src.models import Application
from src.routers.crud import make_crud_router
from src.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate

router = make_crud_router(
    model=Application,
    create_schema=ApplicationCreate,
    update_schema=ApplicationUpdate,
    read_schema=ApplicationRead,
    prefix="/applications",
    tags=["applications"],
)

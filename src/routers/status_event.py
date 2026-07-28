from src.models import StatusEvent
from src.routers.crud import make_crud_router
from src.schemas import StatusEventCreate, StatusEventRead, StatusEventUpdate

router = make_crud_router(
    model=StatusEvent,
    create_schema=StatusEventCreate,
    update_schema=StatusEventUpdate,
    read_schema=StatusEventRead,
    prefix="/status-events",
    tags=["status-events"],
)

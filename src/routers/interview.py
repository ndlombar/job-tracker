from src.models import Interview
from src.routers.crud import make_crud_router
from src.schemas import InterviewCreate, InterviewRead, InterviewUpdate

router = make_crud_router(
    model=Interview,
    create_schema=InterviewCreate,
    update_schema=InterviewUpdate,
    read_schema=InterviewRead,
    prefix="/interviews",
    tags=["interviews"],
)

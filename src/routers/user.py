from src.models import User
from src.routers.crud import make_crud_router
from src.schemas import UserCreate, UserRead, UserUpdate

router = make_crud_router(
    model=User,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    read_schema=UserRead,
    prefix="/users",
    tags=["users"],
)

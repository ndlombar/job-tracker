from src.routers.application import router as application_router
from src.routers.auth import router as auth_router
from src.routers.contact import router as contact_router
from src.routers.interview import router as interview_router
from src.routers.status_event import router as status_event_router
from src.routers.user import router as user_router

__all__ = [
    "application_router",
    "auth_router",
    "contact_router",
    "interview_router",
    "status_event_router",
    "user_router",
]

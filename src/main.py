from fastapi import FastAPI

from src.routers import (
    application_router,
    contact_router,
    interview_router,
    status_event_router,
    user_router,
)

app = FastAPI()

app.include_router(application_router)
app.include_router(contact_router)
app.include_router(interview_router)
app.include_router(status_event_router)
app.include_router(user_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, world!"}
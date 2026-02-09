from fastapi import APIRouter
from src.api.v1.endpoints import auth, users, mail, calendar, drive

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(mail.router, prefix="/mail", tags=["Mail"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(drive.router, prefix="/drive", tags=["Drive"])

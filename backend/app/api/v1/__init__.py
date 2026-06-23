from fastapi import APIRouter
from app.api.v1 import auth, users, counselors, appointments, wellness, chat

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(counselors.router, prefix="/counselors", tags=["Counselors"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(wellness.router, prefix="/wellness", tags=["Wellness"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

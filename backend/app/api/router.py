from fastapi import APIRouter

from app.api.routes import admin, analytics, auth, channels, scheduler, system, videos

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(channels.router)
api_router.include_router(videos.router)
api_router.include_router(scheduler.router)
api_router.include_router(admin.router)
api_router.include_router(analytics.router)
api_router.include_router(system.router)

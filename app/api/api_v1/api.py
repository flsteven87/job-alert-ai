"""
Main API router that includes all endpoint routers.
"""
from fastapi import APIRouter

api_router = APIRouter()

# Import and include routers for different resources
# Note: These endpoints will be implemented later
from app.api.api_v1.endpoints import auth, users, resumes, tracked_pages, jobs, notifications, crawler

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(tracked_pages.router, prefix="/tracked-pages", tags=["tracked-pages"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(crawler.router, prefix="/crawler", tags=["crawler"]) 
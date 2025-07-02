from fastapi import APIRouter
from app.routes import (
    auth_route,
)

api_router = APIRouter()

api_router.include_router(auth_route.router)

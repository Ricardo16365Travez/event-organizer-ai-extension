# Nombre del archivo: app/routes/__init__.py

from fastapi import APIRouter
from app.routes.event_routes import router as event_router
from app.routes.speaker_routes import router as speaker_router
from app.routes.agenda_routes import router as agenda_router
from app.routes.space_routes import router as space_router
from app.routes.user_routes import router as user_router
from app.routes.report_routes import router as report_router

router = APIRouter()

router.include_router(event_router)
router.include_router(speaker_router)
router.include_router(agenda_router)
router.include_router(space_router)
router.include_router(user_router)
router.include_router(report_router)

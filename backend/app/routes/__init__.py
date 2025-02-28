from fastapi import APIRouter

from app.routes.event_routes import router as event_router
from app.routes.speaker_routes import router as speaker_router
from app.routes.agenda_routes import router as agenda_router
from app.routes.space_routes import router as space_router
from app.routes.user_routes import router as user_router

router = APIRouter()

router.include_router(event_router, prefix="/api", tags=["Eventos"])
router.include_router(speaker_router, prefix="/api", tags=["Speakers"])
router.include_router(agenda_router, prefix="/api", tags=["Agendas"])
router.include_router(space_router, prefix="/api", tags=["Espacios"])
router.include_router(user_router, prefix="/api", tags=["Usuarios"])

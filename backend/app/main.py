from fastapi import FastAPI
from app.database import Base, engine
from app.routes import event_routes, speaker_routes, agenda_routes, space_routes, user_routes, report_routes

app = FastAPI(title="Gestor de Eventos con IA")

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Incluir todas las rutas
app.include_router(event_routes.router)
app.include_router(speaker_routes.router)
app.include_router(agenda_routes.router)
app.include_router(space_routes.router)
app.include_router(user_routes.router)
app.include_router(report_routes.router)

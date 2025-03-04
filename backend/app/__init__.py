# Nombre del archivo: app/__init__.py

from fastapi import FastAPI
from app.routes import router
from app.database import Base, engine

# Inicializar la base de datos si aún no existe
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Organizador de Eventos AI",
    description="API para la gestión de eventos, agendas, recomendaciones y reportes.",
    version="1.0.0"
)

# Incluir todas las rutas registradas en app/routes/__init__.py
app.include_router(router)

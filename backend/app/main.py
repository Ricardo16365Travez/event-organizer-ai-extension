from fastapi import FastAPI
from app.routes import router  
from app.routes.event_routes import router as event_router

app = FastAPI()

# Incluir todas las rutas en la aplicación principal
app.include_router(router)
app.include_router(event_router, prefix="/api")
@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}

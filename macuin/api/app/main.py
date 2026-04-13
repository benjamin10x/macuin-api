# api/app/main.py
from fastapi import FastAPI
from app.routers import autopartes, usuarios, pedidos, reportes
from app.data.db import engine
from app.data import models

# Crear tablas al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MACUIN API",
    description="API REST del sistema de autopartes MACUIN - Roberto Carlos Rangel Rodríguez",
    version="1.0.0"
)

# Registrar routers
app.include_router(autopartes.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)
app.include_router(reportes.router)

@app.get("/")
async def root():
    return {"mensaje": "MACUIN API funcionando", "version": "1.0.0"}

"""
main.py
-------
Punto de entrada de la aplicación FastAPI.

Sistema de Gestión de Citas Médicas y Automatización de Caja Contable.

Aquí se:
- Crea la instancia de FastAPI con su metadata (título, descripción, versión).
- Crean automáticamente las tablas de SQLite al iniciar.
- Registran (incluyen) todos los routers/controladores de los módulos.

Ejecución local:
    uvicorn main:app --reload

Documentación Swagger:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# Importamos los modelos para que SQLAlchemy conozca las tablas a crear.
from models import paciente_model, medico_model, cita_model, consulta_model, certificado_model  # noqa: F401

# Importamos los controladores (routers) de cada módulo.
from controllers import (
    paciente_controller,
    medico_controller,
    cita_controller,
    consulta_controller,
    certificado_controller,
    reporte_controller,
)

# Crea automáticamente todas las tablas en SQLite si aún no existen.
Base.metadata.create_all(bind=engine)

# Instancia principal de la aplicación con metadata para Swagger.
app = FastAPI(
    title="Sistema de Gestión de Citas Médicas",
    description=(
        "Backend para la gestión de pacientes, médicos, citas, consultas, "
        "certificados médicos y reportes. Desarrollado con FastAPI, SQLAlchemy "
        "y SQLite siguiendo una arquitectura Modelo / Repositorio / Servicio / Controlador."
    ),
    version="1.0.0",
    contact={"name": "Maydene Alejandra Madero Lascano"},
)

# Configuración de CORS (permite consumir la API desde cualquier origen).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Inicio"], summary="Estado del API")
def inicio():
    """Endpoint de bienvenida para verificar que el API está en línea."""
    return {
        "mensaje": "API del Sistema de Gestión de Citas Médicas en funcionamiento.",
        "documentacion": "/docs",
    }


# Registro de todos los routers de los módulos del sistema.
app.include_router(paciente_controller.router)
app.include_router(medico_controller.router)
app.include_router(cita_controller.router)
app.include_router(consulta_controller.router)
app.include_router(certificado_controller.router)
app.include_router(reporte_controller.router)

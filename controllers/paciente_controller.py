"""
paciente_controller.py
----------------------
Controlador (rutas REST) del módulo Pacientes.

Expone los endpoints HTTP y delega la lógica a la capa de servicio.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.paciente_schema import PacienteCreate, PacienteUpdate, PacienteResponse
from services import paciente_service

# Prefijo común y etiqueta para agrupar en Swagger.
router = APIRouter(prefix="/api/pacientes", tags=["Pacientes"])


@router.post("", response_model=PacienteResponse, summary="Crear paciente")
def crear_paciente(datos: PacienteCreate, db: Session = Depends(get_db)):
    """Registra un nuevo paciente en el sistema."""
    return paciente_service.crear_paciente(db, datos)


@router.get("", response_model=List[PacienteResponse], summary="Listar pacientes")
def listar_pacientes(db: Session = Depends(get_db)):
    """Devuelve todos los pacientes registrados."""
    return paciente_service.listar_pacientes(db)


@router.get("/{paciente_id}", response_model=PacienteResponse, summary="Obtener paciente por id")
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtiene los datos de un paciente por su id."""
    return paciente_service.obtener_paciente(db, paciente_id)


@router.put("/{paciente_id}", response_model=PacienteResponse, summary="Actualizar paciente")
def actualizar_paciente(paciente_id: int, datos: PacienteUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un paciente existente."""
    return paciente_service.actualizar_paciente(db, paciente_id, datos)


@router.delete("/{paciente_id}", summary="Eliminar paciente")
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Elimina un paciente del sistema."""
    return paciente_service.eliminar_paciente(db, paciente_id)

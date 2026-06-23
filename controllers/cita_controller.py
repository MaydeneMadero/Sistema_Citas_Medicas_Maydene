"""
cita_controller.py
------------------
Controlador (rutas REST) del módulo Citas.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.cita_schema import CitaCreate, CitaUpdate, CitaResponse
from services import cita_service

router = APIRouter(prefix="/api/citas", tags=["Citas"])


@router.post("", response_model=CitaResponse, summary="Crear cita")
def crear_cita(datos: CitaCreate, db: Session = Depends(get_db)):
    """Crea una cita (estado inicial PENDIENTE). Valida paciente y médico."""
    return cita_service.crear_cita(db, datos)


@router.get("", response_model=List[CitaResponse], summary="Listar citas")
def listar_citas(db: Session = Depends(get_db)):
    """Devuelve todas las citas registradas."""
    return cita_service.listar_citas(db)


# IMPORTANTE: esta ruta se define antes de "/{cita_id}" para evitar conflictos.
@router.get("/paciente/{cedula}", response_model=List[CitaResponse], summary="Citas por cédula de paciente")
def listar_citas_por_cedula(cedula: str, db: Session = Depends(get_db)):
    """Devuelve las citas de un paciente buscando por su cédula."""
    return cita_service.listar_citas_por_cedula(db, cedula)


@router.get("/{cita_id}", response_model=CitaResponse, summary="Obtener cita por id")
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    """Obtiene los datos de una cita por su id."""
    return cita_service.obtener_cita(db, cita_id)


@router.put("/{cita_id}", response_model=CitaResponse, summary="Actualizar cita")
def actualizar_cita(cita_id: int, datos: CitaUpdate, db: Session = Depends(get_db)):
    """Actualiza una cita (incluido su estado, validado)."""
    return cita_service.actualizar_cita(db, cita_id, datos)


@router.delete("/{cita_id}", summary="Eliminar cita")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    """Elimina una cita del sistema."""
    return cita_service.eliminar_cita(db, cita_id)

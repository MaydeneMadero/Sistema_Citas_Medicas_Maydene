"""
medico_controller.py
--------------------
Controlador (rutas REST) del módulo Médicos.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.medico_schema import MedicoCreate, MedicoUpdate, MedicoResponse
from services import medico_service

router = APIRouter(prefix="/api/medicos", tags=["Médicos"])


@router.post("", response_model=MedicoResponse, summary="Crear médico")
def crear_medico(datos: MedicoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo médico o colaborador."""
    return medico_service.crear_medico(db, datos)


@router.get("", response_model=List[MedicoResponse], summary="Listar médicos")
def listar_medicos(db: Session = Depends(get_db)):
    """Devuelve todos los médicos registrados."""
    return medico_service.listar_medicos(db)


@router.get("/{medico_id}", response_model=MedicoResponse, summary="Obtener médico por id")
def obtener_medico(medico_id: int, db: Session = Depends(get_db)):
    """Obtiene los datos de un médico por su id."""
    return medico_service.obtener_medico(db, medico_id)


@router.put("/{medico_id}", response_model=MedicoResponse, summary="Actualizar médico")
def actualizar_medico(medico_id: int, datos: MedicoUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un médico existente."""
    return medico_service.actualizar_medico(db, medico_id, datos)


@router.delete("/{medico_id}", summary="Eliminar médico")
def eliminar_medico(medico_id: int, db: Session = Depends(get_db)):
    """Elimina un médico del sistema."""
    return medico_service.eliminar_medico(db, medico_id)

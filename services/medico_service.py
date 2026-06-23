"""
medico_service.py
-----------------
Capa de servicio del módulo Médicos.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import medico_repository
from schemas.medico_schema import MedicoCreate, MedicoUpdate


def crear_medico(db: Session, datos: MedicoCreate):
    """Crea un médico validando que la cédula no esté repetida."""
    existente = medico_repository.obtener_por_cedula(db, datos.cedula)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un médico con la cédula {datos.cedula}.",
        )
    return medico_repository.crear(db, datos)


def listar_medicos(db: Session):
    """Devuelve la lista completa de médicos."""
    return medico_repository.listar(db)


def obtener_medico(db: Session, medico_id: int):
    """Obtiene un médico por id o lanza error 404 si no existe."""
    medico = medico_repository.obtener_por_id(db, medico_id)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el médico con id {medico_id}.",
        )
    return medico


def actualizar_medico(db: Session, medico_id: int, datos: MedicoUpdate):
    """Actualiza los datos de un médico existente."""
    medico = obtener_medico(db, medico_id)
    return medico_repository.actualizar(db, medico, datos)


def eliminar_medico(db: Session, medico_id: int):
    """Elimina un médico existente."""
    medico = obtener_medico(db, medico_id)
    medico_repository.eliminar(db, medico)
    return {"mensaje": f"Médico con id {medico_id} eliminado correctamente."}

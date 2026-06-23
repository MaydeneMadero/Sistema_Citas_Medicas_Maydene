"""
consulta_service.py
-------------------
Capa de servicio del módulo Consultas Médicas.

Regla funcional: para registrar una consulta, la cita debe existir.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import consulta_repository, cita_repository, paciente_repository
from schemas.consulta_schema import ConsultaCreate


def crear_consulta(db: Session, datos: ConsultaCreate):
    """Registra una consulta validando que la cita exista."""

    # Regla 5: la cita debe existir.
    cita = cita_repository.obtener_por_id(db, datos.cita_id)
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede registrar la consulta: la cita con id {datos.cita_id} no existe.",
        )

    consulta = consulta_repository.crear(db, datos)

    # Al registrar la consulta, la cita pasa automáticamente a ATENDIDA.
    cita.estado = "ATENDIDA"
    cita_repository.actualizar(db, cita)

    return consulta


def listar_consultas(db: Session):
    """Devuelve la lista completa de consultas."""
    return consulta_repository.listar(db)


def obtener_consulta(db: Session, consulta_id: int):
    """Obtiene una consulta por id o lanza error 404 si no existe."""
    consulta = consulta_repository.obtener_por_id(db, consulta_id)
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la consulta con id {consulta_id}.",
        )
    return consulta


def listar_consultas_por_cedula(db: Session, cedula: str):
    """Devuelve las consultas de un paciente buscando por su cédula."""
    paciente = paciente_repository.obtener_por_cedula(db, cedula)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con la cédula {cedula}.",
        )
    return consulta_repository.listar_por_cedula_paciente(db, cedula)

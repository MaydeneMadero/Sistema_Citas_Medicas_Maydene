"""
paciente_service.py
-------------------
Capa de servicio del módulo Pacientes.

Contiene las reglas de negocio y validaciones. Lanza HTTPException con
mensajes claros cuando los datos no cumplen las condiciones esperadas.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import paciente_repository
from schemas.paciente_schema import PacienteCreate, PacienteUpdate


def crear_paciente(db: Session, datos: PacienteCreate):
    """Crea un paciente validando que la cédula no esté repetida."""
    existente = paciente_repository.obtener_por_cedula(db, datos.cedula)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un paciente con la cédula {datos.cedula}.",
        )
    return paciente_repository.crear(db, datos)


def listar_pacientes(db: Session):
    """Devuelve la lista completa de pacientes."""
    return paciente_repository.listar(db)


def obtener_paciente(db: Session, paciente_id: int):
    """Obtiene un paciente por id o lanza error 404 si no existe."""
    paciente = paciente_repository.obtener_por_id(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el paciente con id {paciente_id}.",
        )
    return paciente


def actualizar_paciente(db: Session, paciente_id: int, datos: PacienteUpdate):
    """Actualiza los datos de un paciente existente."""
    paciente = obtener_paciente(db, paciente_id)
    return paciente_repository.actualizar(db, paciente, datos)


def eliminar_paciente(db: Session, paciente_id: int):
    """Elimina un paciente existente."""
    paciente = obtener_paciente(db, paciente_id)
    paciente_repository.eliminar(db, paciente)
    return {"mensaje": f"Paciente con id {paciente_id} eliminado correctamente."}

"""
certificado_service.py
----------------------
Capa de servicio del módulo Certificados Médicos.

Valida que el paciente y el médico existan antes de emitir el certificado.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import certificado_repository, paciente_repository, medico_repository
from schemas.certificado_schema import CertificadoCreate


def crear_certificado(db: Session, datos: CertificadoCreate):
    """Emite un certificado validando que el paciente y el médico existan."""

    # El paciente debe existir.
    if not paciente_repository.obtener_por_id(db, datos.paciente_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede emitir el certificado: el paciente con id {datos.paciente_id} no existe.",
        )

    # El médico debe existir.
    if not medico_repository.obtener_por_id(db, datos.medico_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede emitir el certificado: el médico con id {datos.medico_id} no existe.",
        )

    return certificado_repository.crear(db, datos)


def listar_certificados(db: Session):
    """Devuelve la lista completa de certificados."""
    return certificado_repository.listar(db)


def obtener_certificado(db: Session, certificado_id: int):
    """Obtiene un certificado por id o lanza error 404 si no existe."""
    certificado = certificado_repository.obtener_por_id(db, certificado_id)
    if not certificado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el certificado con id {certificado_id}.",
        )
    return certificado


def listar_certificados_por_cedula(db: Session, cedula: str):
    """Devuelve los certificados de un paciente buscando por su cédula."""
    paciente = paciente_repository.obtener_por_cedula(db, cedula)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con la cédula {cedula}.",
        )
    return certificado_repository.listar_por_cedula_paciente(db, cedula)

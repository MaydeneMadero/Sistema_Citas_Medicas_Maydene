"""
certificado_controller.py
-------------------------
Controlador (rutas REST) del módulo Certificados Médicos.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.certificado_schema import CertificadoCreate, CertificadoResponse
from services import certificado_service

router = APIRouter(prefix="/api/certificados", tags=["Certificados"])


@router.post("", response_model=CertificadoResponse, summary="Emitir certificado")
def crear_certificado(datos: CertificadoCreate, db: Session = Depends(get_db)):
    """Emite un certificado médico. Valida paciente y médico."""
    return certificado_service.crear_certificado(db, datos)


@router.get("", response_model=List[CertificadoResponse], summary="Listar certificados")
def listar_certificados(db: Session = Depends(get_db)):
    """Devuelve todos los certificados registrados."""
    return certificado_service.listar_certificados(db)


# Ruta por cédula antes de "/{certificado_id}" para evitar conflictos.
@router.get("/paciente/{cedula}", response_model=List[CertificadoResponse], summary="Certificados por cédula de paciente")
def listar_certificados_por_cedula(cedula: str, db: Session = Depends(get_db)):
    """Devuelve los certificados de un paciente buscando por su cédula."""
    return certificado_service.listar_certificados_por_cedula(db, cedula)


@router.get("/{certificado_id}", response_model=CertificadoResponse, summary="Obtener certificado por id")
def obtener_certificado(certificado_id: int, db: Session = Depends(get_db)):
    """Obtiene los datos de un certificado por su id."""
    return certificado_service.obtener_certificado(db, certificado_id)

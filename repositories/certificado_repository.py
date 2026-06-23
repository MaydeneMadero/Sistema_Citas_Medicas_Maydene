"""
certificado_repository.py
-------------------------
Capa de acceso a datos del módulo Certificados Médicos.
"""

from sqlalchemy.orm import Session

from models.certificado_model import CertificadoMedico
from models.paciente_model import Paciente
from schemas.certificado_schema import CertificadoCreate


def crear(db: Session, datos: CertificadoCreate) -> CertificadoMedico:
    """Inserta un nuevo certificado médico."""
    certificado = CertificadoMedico(**datos.model_dump())
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def listar(db: Session):
    """Devuelve todos los certificados médicos."""
    return db.query(CertificadoMedico).all()


def obtener_por_id(db: Session, certificado_id: int):
    """Busca un certificado por su id."""
    return db.query(CertificadoMedico).filter(CertificadoMedico.id == certificado_id).first()


def listar_por_cedula_paciente(db: Session, cedula: str):
    """
    Devuelve los certificados de un paciente buscando por su cédula.
    Se hace un JOIN con la tabla de pacientes.
    """
    return (
        db.query(CertificadoMedico)
        .join(Paciente, CertificadoMedico.paciente_id == Paciente.id)
        .filter(Paciente.cedula == cedula)
        .all()
    )

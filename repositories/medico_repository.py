"""
medico_repository.py
--------------------
Capa de acceso a datos del módulo Médicos.
"""

from sqlalchemy.orm import Session

from models.medico_model import Medico
from schemas.medico_schema import MedicoCreate, MedicoUpdate


def crear(db: Session, datos: MedicoCreate) -> Medico:
    """Inserta un nuevo médico en la base de datos."""
    medico = Medico(**datos.model_dump())
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico


def listar(db: Session):
    """Devuelve todos los médicos registrados."""
    return db.query(Medico).all()


def obtener_por_id(db: Session, medico_id: int):
    """Busca un médico por su id."""
    return db.query(Medico).filter(Medico.id == medico_id).first()


def obtener_por_cedula(db: Session, cedula: str):
    """Busca un médico por su cédula."""
    return db.query(Medico).filter(Medico.cedula == cedula).first()


def actualizar(db: Session, medico: Medico, datos: MedicoUpdate) -> Medico:
    """Actualiza solo los campos enviados (no nulos) de un médico."""
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(medico, campo, valor)
    db.commit()
    db.refresh(medico)
    return medico


def eliminar(db: Session, medico: Medico) -> None:
    """Elimina un médico de la base de datos."""
    db.delete(medico)
    db.commit()

"""
consulta_repository.py
----------------------
Capa de acceso a datos del módulo Consultas Médicas.
"""

from sqlalchemy.orm import Session

from models.consulta_model import ConsultaMedica
from models.cita_model import Cita
from models.paciente_model import Paciente
from schemas.consulta_schema import ConsultaCreate


def crear(db: Session, datos: ConsultaCreate) -> ConsultaMedica:
    """Inserta una nueva consulta médica."""
    consulta = ConsultaMedica(**datos.model_dump())
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


def listar(db: Session):
    """Devuelve todas las consultas médicas."""
    return db.query(ConsultaMedica).all()


def obtener_por_id(db: Session, consulta_id: int):
    """Busca una consulta por su id."""
    return db.query(ConsultaMedica).filter(ConsultaMedica.id == consulta_id).first()


def listar_por_cedula_paciente(db: Session, cedula: str):
    """
    Devuelve las consultas de un paciente buscando por su cédula.
    Se hacen JOINs: Consulta -> Cita -> Paciente.
    """
    return (
        db.query(ConsultaMedica)
        .join(Cita, ConsultaMedica.cita_id == Cita.id)
        .join(Paciente, Cita.paciente_id == Paciente.id)
        .filter(Paciente.cedula == cedula)
        .all()
    )

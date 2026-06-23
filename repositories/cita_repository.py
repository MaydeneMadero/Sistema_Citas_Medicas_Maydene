"""
cita_repository.py
------------------
Capa de acceso a datos del módulo Citas.
"""

from sqlalchemy.orm import Session

from models.cita_model import Cita
from models.paciente_model import Paciente


def crear(db: Session, cita: Cita) -> Cita:
    """Inserta una cita ya construida (el estado se asigna en el servicio)."""
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


def listar(db: Session):
    """Devuelve todas las citas registradas."""
    return db.query(Cita).all()


def obtener_por_id(db: Session, cita_id: int):
    """Busca una cita por su id."""
    return db.query(Cita).filter(Cita.id == cita_id).first()


def listar_por_estado(db: Session, estado: str):
    """Devuelve las citas que tengan un estado específico."""
    return db.query(Cita).filter(Cita.estado == estado).all()


def listar_por_cedula_paciente(db: Session, cedula: str):
    """
    Devuelve las citas de un paciente buscando por su cédula.
    Se hace un JOIN con la tabla de pacientes.
    """
    return (
        db.query(Cita)
        .join(Paciente, Cita.paciente_id == Paciente.id)
        .filter(Paciente.cedula == cedula)
        .all()
    )


def actualizar(db: Session, cita: Cita) -> Cita:
    """Guarda los cambios realizados sobre una cita."""
    db.commit()
    db.refresh(cita)
    return cita


def eliminar(db: Session, cita: Cita) -> None:
    """Elimina una cita de la base de datos."""
    db.delete(cita)
    db.commit()

"""
paciente_repository.py
----------------------
Capa de acceso a datos del módulo Pacientes.

El repositorio se encarga ÚNICAMENTE de interactuar con la base de datos
(consultas, insertar, actualizar, eliminar). No contiene reglas de negocio.
"""

from sqlalchemy.orm import Session

from models.paciente_model import Paciente
from schemas.paciente_schema import PacienteCreate, PacienteUpdate


def crear(db: Session, datos: PacienteCreate) -> Paciente:
    """Inserta un nuevo paciente en la base de datos."""
    paciente = Paciente(**datos.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


def listar(db: Session):
    """Devuelve todos los pacientes registrados."""
    return db.query(Paciente).all()


def obtener_por_id(db: Session, paciente_id: int):
    """Busca un paciente por su id."""
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()


def obtener_por_cedula(db: Session, cedula: str):
    """Busca un paciente por su cédula."""
    return db.query(Paciente).filter(Paciente.cedula == cedula).first()


def actualizar(db: Session, paciente: Paciente, datos: PacienteUpdate) -> Paciente:
    """Actualiza solo los campos enviados (no nulos) de un paciente."""
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(paciente, campo, valor)
    db.commit()
    db.refresh(paciente)
    return paciente


def eliminar(db: Session, paciente: Paciente) -> None:
    """Elimina un paciente de la base de datos."""
    db.delete(paciente)
    db.commit()

"""
cita_model.py
-------------
Modelo (tabla) que representa una Cita Médica.

El estado de una cita solo puede ser: PENDIENTE, ATENDIDA o CANCELADA.
El estado inicial siempre es PENDIENTE.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Cita(Base):
    """Tabla 'citas': relaciona a un paciente con un médico en una fecha/hora."""

    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    fecha = Column(String, nullable=False)  # Formato: YYYY-MM-DD
    hora = Column(String, nullable=False)   # Formato: HH:MM
    motivo = Column(String, nullable=True)
    # Estado inicial PENDIENTE. Valores válidos: PENDIENTE, ATENDIDA, CANCELADA.
    estado = Column(String, default="PENDIENTE", nullable=False)

    # Relaciones con paciente, médico y consulta.
    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
    consulta = relationship("ConsultaMedica", back_populates="cita", uselist=False)

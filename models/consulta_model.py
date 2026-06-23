"""
consulta_model.py
-----------------
Modelo (tabla) que representa una Consulta Médica.

Una consulta está asociada a una cita existente y guarda el detalle
clínico de la atención: diagnóstico, tratamiento, prescripción, etc.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ConsultaMedica(Base):
    """Tabla 'consultas': detalle clínico de la atención de una cita."""

    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey("citas.id"), nullable=False)
    diagnostico = Column(String, nullable=True)
    tratamiento = Column(String, nullable=True)
    prescripcion = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    # Fecha de registro generada automáticamente al crear la consulta.
    fecha_registro = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Relación con la cita a la que pertenece.
    cita = relationship("Cita", back_populates="consulta")

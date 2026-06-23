"""
certificado_model.py
--------------------
Modelo (tabla) que representa un Certificado Médico emitido por un médico
a un paciente.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class CertificadoMedico(Base):
    """Tabla 'certificados': documentos médicos emitidos a un paciente."""

    __tablename__ = "certificados"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    descripcion = Column(String, nullable=False)
    # Fecha de emisión generada automáticamente al crear el certificado.
    fecha_emision = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Relaciones con paciente y médico.
    paciente = relationship("Paciente", back_populates="certificados")
    medico = relationship("Medico", back_populates="certificados")

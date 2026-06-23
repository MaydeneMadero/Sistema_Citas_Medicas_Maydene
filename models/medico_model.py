"""
medico_model.py
---------------
Modelo (tabla) que representa a un Médico o Colaborador del sistema.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Medico(Base):
    """Tabla 'medicos': almacena los datos de los médicos o colaboradores."""

    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    especialidad = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    correo = Column(String, nullable=True)
    # Estado del médico: ACTIVO / INACTIVO (por defecto ACTIVO).
    estado = Column(String, default="ACTIVO", nullable=False)

    # Relaciones: un médico puede tener muchas citas y certificados.
    citas = relationship("Cita", back_populates="medico")
    certificados = relationship("CertificadoMedico", back_populates="medico")

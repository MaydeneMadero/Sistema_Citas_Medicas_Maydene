"""
paciente_model.py
-----------------
Modelo (tabla) que representa a un Paciente dentro del sistema.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Paciente(Base):
    """Tabla 'pacientes': almacena los datos personales de cada paciente."""

    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    fecha_nacimiento = Column(String, nullable=True)  # Formato: YYYY-MM-DD
    telefono = Column(String, nullable=True)
    correo = Column(String, nullable=True)
    direccion = Column(String, nullable=True)

    # Relaciones: un paciente puede tener muchas citas y certificados.
    citas = relationship("Cita", back_populates="paciente")
    certificados = relationship("CertificadoMedico", back_populates="paciente")

"""
cita_schema.py
--------------
Esquemas Pydantic para el módulo de Citas Médicas.

Se define un Enum con los estados válidos para garantizar que una cita
solo pueda tener uno de los valores permitidos.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EstadoCita(str, Enum):
    """Estados permitidos para una cita médica."""

    PENDIENTE = "PENDIENTE"
    ATENDIDA = "ATENDIDA"
    CANCELADA = "CANCELADA"


class CitaBase(BaseModel):
    """Campos comunes de una cita."""

    paciente_id: int = Field(..., description="ID del paciente existente")
    medico_id: int = Field(..., description="ID del médico existente")
    fecha: str = Field(..., description="Formato YYYY-MM-DD")
    hora: str = Field(..., description="Formato HH:MM")
    motivo: Optional[str] = None


class CitaCreate(CitaBase):
    """Esquema para crear una cita. El estado inicial se asigna en el servicio."""
    pass


class CitaUpdate(BaseModel):
    """Esquema para actualizar una cita. Todos los campos son opcionales."""

    paciente_id: Optional[int] = None
    medico_id: Optional[int] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    motivo: Optional[str] = None
    estado: Optional[EstadoCita] = None


class CitaResponse(CitaBase):
    """Esquema de respuesta: incluye id y estado actual."""

    id: int
    estado: EstadoCita

    class Config:
        from_attributes = True

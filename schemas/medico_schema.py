"""
medico_schema.py
----------------
Esquemas Pydantic para el módulo de Médicos / Colaboradores.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class MedicoBase(BaseModel):
    """Campos comunes de un médico."""

    cedula: str = Field(..., min_length=1, description="Cédula única del médico")
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = Field("ACTIVO", description="ACTIVO o INACTIVO")


class MedicoCreate(MedicoBase):
    """Esquema para crear un médico."""
    pass


class MedicoUpdate(BaseModel):
    """Esquema para actualizar un médico. Todos los campos son opcionales."""

    cedula: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = None


class MedicoResponse(MedicoBase):
    """Esquema de respuesta: incluye el id generado."""

    id: int

    class Config:
        from_attributes = True

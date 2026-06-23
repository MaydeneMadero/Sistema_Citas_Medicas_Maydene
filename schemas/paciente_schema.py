"""
paciente_schema.py
------------------
Esquemas Pydantic para el módulo de Pacientes.

Definen la forma de los datos que entran (creación/actualización) y
salen (respuesta) del API, incluyendo validaciones básicas.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class PacienteBase(BaseModel):
    """Campos comunes de un paciente."""

    cedula: str = Field(..., min_length=1, description="Cédula única del paciente")
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    fecha_nacimiento: Optional[str] = Field(None, description="Formato YYYY-MM-DD")
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = None


class PacienteCreate(PacienteBase):
    """Esquema para crear un paciente (mismos campos que la base)."""
    pass


class PacienteUpdate(BaseModel):
    """Esquema para actualizar un paciente. Todos los campos son opcionales."""

    cedula: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = None


class PacienteResponse(PacienteBase):
    """Esquema de respuesta: incluye el id generado por la base de datos."""

    id: int

    class Config:
        from_attributes = True  # Permite construir el esquema desde el modelo ORM.

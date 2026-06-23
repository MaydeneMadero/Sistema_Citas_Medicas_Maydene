"""
consulta_schema.py
------------------
Esquemas Pydantic para el módulo de Consultas Médicas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ConsultaBase(BaseModel):
    """Campos comunes de una consulta médica."""

    cita_id: int = Field(..., description="ID de la cita existente")
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    prescripcion: Optional[str] = None
    observaciones: Optional[str] = None


class ConsultaCreate(ConsultaBase):
    """Esquema para registrar una consulta médica."""
    pass


class ConsultaResponse(ConsultaBase):
    """Esquema de respuesta: incluye id y fecha de registro."""

    id: int
    fecha_registro: Optional[str] = None

    class Config:
        from_attributes = True

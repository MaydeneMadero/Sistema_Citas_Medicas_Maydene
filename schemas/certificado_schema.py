"""
certificado_schema.py
---------------------
Esquemas Pydantic para el módulo de Certificados Médicos.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CertificadoBase(BaseModel):
    """Campos comunes de un certificado médico."""

    paciente_id: int = Field(..., description="ID del paciente existente")
    medico_id: int = Field(..., description="ID del médico existente")
    descripcion: str = Field(..., min_length=1)


class CertificadoCreate(CertificadoBase):
    """Esquema para emitir un certificado médico."""
    pass


class CertificadoResponse(CertificadoBase):
    """Esquema de respuesta: incluye id y fecha de emisión."""

    id: int
    fecha_emision: Optional[str] = None

    class Config:
        from_attributes = True

"""
consulta_controller.py
----------------------
Controlador (rutas REST) del módulo Consultas Médicas.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.consulta_schema import ConsultaCreate, ConsultaResponse
from services import consulta_service

router = APIRouter(prefix="/api/consultas", tags=["Consultas"])


@router.post("", response_model=ConsultaResponse, summary="Registrar consulta")
def crear_consulta(datos: ConsultaCreate, db: Session = Depends(get_db)):
    """Registra una consulta médica. La cita debe existir."""
    return consulta_service.crear_consulta(db, datos)


@router.get("", response_model=List[ConsultaResponse], summary="Listar consultas")
def listar_consultas(db: Session = Depends(get_db)):
    """Devuelve todas las consultas registradas."""
    return consulta_service.listar_consultas(db)


# Ruta por cédula antes de "/{consulta_id}" para evitar conflictos.
@router.get("/paciente/{cedula}", response_model=List[ConsultaResponse], summary="Consultas por cédula de paciente")
def listar_consultas_por_cedula(cedula: str, db: Session = Depends(get_db)):
    """Devuelve las consultas de un paciente buscando por su cédula."""
    return consulta_service.listar_consultas_por_cedula(db, cedula)


@router.get("/{consulta_id}", response_model=ConsultaResponse, summary="Obtener consulta por id")
def obtener_consulta(consulta_id: int, db: Session = Depends(get_db)):
    """Obtiene los datos de una consulta por su id."""
    return consulta_service.obtener_consulta(db, consulta_id)

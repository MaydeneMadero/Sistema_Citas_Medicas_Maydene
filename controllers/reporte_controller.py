"""
reporte_controller.py
---------------------
Controlador (rutas REST) del módulo de Reportes básicos.

Incluye:
- Historia clínica completa de un paciente (por cédula).
- Resumen general de citas por estado.
- Listado de citas filtradas por un estado específico.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from repositories import (
    paciente_repository,
    cita_repository,
    consulta_repository,
    certificado_repository,
)
from schemas.cita_schema import EstadoCita

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


@router.get("/historia-clinica/{cedula}", summary="Historia clínica del paciente")
def historia_clinica(cedula: str, db: Session = Depends(get_db)):
    """
    Devuelve la historia clínica de un paciente: sus datos personales,
    sus citas atendidas, las consultas con diagnósticos y tratamientos,
    y los certificados emitidos.
    """
    paciente = paciente_repository.obtener_por_cedula(db, cedula)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con la cédula {cedula}.",
        )

    # Citas del paciente y filtrado de las atendidas.
    citas = cita_repository.listar_por_cedula_paciente(db, cedula)
    citas_atendidas = [c for c in citas if c.estado == "ATENDIDA"]

    # Consultas y certificados del paciente.
    consultas = consulta_repository.listar_por_cedula_paciente(db, cedula)
    certificados = certificado_repository.listar_por_cedula_paciente(db, cedula)

    return {
        "paciente": {
            "id": paciente.id,
            "cedula": paciente.cedula,
            "nombres": paciente.nombres,
            "apellidos": paciente.apellidos,
            "fecha_nacimiento": paciente.fecha_nacimiento,
            "telefono": paciente.telefono,
            "correo": paciente.correo,
            "direccion": paciente.direccion,
        },
        "total_citas": len(citas),
        "citas_atendidas": [
            {
                "id": c.id,
                "fecha": c.fecha,
                "hora": c.hora,
                "motivo": c.motivo,
                "estado": c.estado,
                "medico_id": c.medico_id,
            }
            for c in citas_atendidas
        ],
        "consultas": [
            {
                "id": co.id,
                "cita_id": co.cita_id,
                "diagnostico": co.diagnostico,
                "tratamiento": co.tratamiento,
                "prescripcion": co.prescripcion,
                "observaciones": co.observaciones,
                "fecha_registro": co.fecha_registro,
            }
            for co in consultas
        ],
        "certificados": [
            {
                "id": ce.id,
                "descripcion": ce.descripcion,
                "fecha_emision": ce.fecha_emision,
                "medico_id": ce.medico_id,
            }
            for ce in certificados
        ],
    }


@router.get("/resumen-citas", summary="Resumen de citas por estado")
def resumen_citas(db: Session = Depends(get_db)):
    """Devuelve el total de citas y cuántas hay en cada estado."""
    citas = cita_repository.listar(db)
    resumen = {
        "total": len(citas),
        "pendientes": len([c for c in citas if c.estado == "PENDIENTE"]),
        "atendidas": len([c for c in citas if c.estado == "ATENDIDA"]),
        "canceladas": len([c for c in citas if c.estado == "CANCELADA"]),
    }
    return resumen


@router.get("/citas-por-estado/{estado}", summary="Citas filtradas por estado")
def citas_por_estado(estado: str, db: Session = Depends(get_db)):
    """Devuelve las citas que se encuentran en el estado indicado."""
    estado_mayus = estado.upper()
    # Validar que el estado solicitado sea válido.
    if estado_mayus not in [e.value for e in EstadoCita]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estado debe ser PENDIENTE, ATENDIDA o CANCELADA.",
        )

    citas = cita_repository.listar_por_estado(db, estado_mayus)
    return {
        "estado": estado_mayus,
        "total": len(citas),
        "citas": [
            {
                "id": c.id,
                "paciente_id": c.paciente_id,
                "medico_id": c.medico_id,
                "fecha": c.fecha,
                "hora": c.hora,
                "motivo": c.motivo,
                "estado": c.estado,
            }
            for c in citas
        ],
    }

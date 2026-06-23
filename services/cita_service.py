"""
cita_service.py
---------------
Capa de servicio del módulo Citas.

Aquí se aplican las reglas funcionales más importantes:
- No se crea una cita si el paciente no existe.
- No se crea una cita si el médico no existe.
- El estado inicial de una cita es PENDIENTE.
- Una cita solo puede estar en PENDIENTE, ATENDIDA o CANCELADA.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.cita_model import Cita
from repositories import cita_repository, paciente_repository, medico_repository
from schemas.cita_schema import CitaCreate, CitaUpdate, EstadoCita


def crear_cita(db: Session, datos: CitaCreate):
    """Crea una cita validando paciente y médico, y asignando estado PENDIENTE."""

    # Regla 1: el paciente debe existir.
    paciente = paciente_repository.obtener_por_id(db, datos.paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la cita: el paciente con id {datos.paciente_id} no existe.",
        )

    # Regla 2: el médico debe existir.
    medico = medico_repository.obtener_por_id(db, datos.medico_id)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la cita: el médico con id {datos.medico_id} no existe.",
        )

    # Regla 3: el estado inicial siempre es PENDIENTE.
    cita = Cita(
        paciente_id=datos.paciente_id,
        medico_id=datos.medico_id,
        fecha=datos.fecha,
        hora=datos.hora,
        motivo=datos.motivo,
        estado=EstadoCita.PENDIENTE.value,
    )
    return cita_repository.crear(db, cita)


def listar_citas(db: Session):
    """Devuelve la lista completa de citas."""
    return cita_repository.listar(db)


def obtener_cita(db: Session, cita_id: int):
    """Obtiene una cita por id o lanza error 404 si no existe."""
    cita = cita_repository.obtener_por_id(db, cita_id)
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la cita con id {cita_id}.",
        )
    return cita


def listar_citas_por_cedula(db: Session, cedula: str):
    """Devuelve las citas de un paciente buscando por su cédula."""
    paciente = paciente_repository.obtener_por_cedula(db, cedula)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un paciente con la cédula {cedula}.",
        )
    return cita_repository.listar_por_cedula_paciente(db, cedula)


def actualizar_cita(db: Session, cita_id: int, datos: CitaUpdate):
    """Actualiza una cita validando paciente, médico y estado si se envían."""
    cita = obtener_cita(db, cita_id)
    cambios = datos.model_dump(exclude_unset=True)

    # Si cambia el paciente, validar que exista.
    if "paciente_id" in cambios:
        if not paciente_repository.obtener_por_id(db, cambios["paciente_id"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El paciente con id {cambios['paciente_id']} no existe.",
            )

    # Si cambia el médico, validar que exista.
    if "medico_id" in cambios:
        if not medico_repository.obtener_por_id(db, cambios["medico_id"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El médico con id {cambios['medico_id']} no existe.",
            )

    # Regla 4: el estado debe ser uno de los valores válidos.
    if "estado" in cambios and cambios["estado"] is not None:
        estado_valor = cambios["estado"]
        # El valor puede venir como Enum o como texto.
        estado_texto = estado_valor.value if isinstance(estado_valor, EstadoCita) else estado_valor
        if estado_texto not in [e.value for e in EstadoCita]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado debe ser PENDIENTE, ATENDIDA o CANCELADA.",
            )
        cambios["estado"] = estado_texto

    # Aplicar los cambios sobre el objeto cita.
    for campo, valor in cambios.items():
        setattr(cita, campo, valor)

    return cita_repository.actualizar(db, cita)


def eliminar_cita(db: Session, cita_id: int):
    """Elimina una cita existente."""
    cita = obtener_cita(db, cita_id)
    cita_repository.eliminar(db, cita)
    return {"mensaje": f"Cita con id {cita_id} eliminada correctamente."}

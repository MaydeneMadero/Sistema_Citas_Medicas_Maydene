"""
database.py
-----------
Configuración central de la base de datos del sistema.

Se utiliza SQLAlchemy como ORM y SQLite como motor de base de datos
para facilitar la ejecución local sin necesidad de instalar servidores
externos. El archivo de base de datos (citas_medicas.db) se crea
automáticamente en la raíz del proyecto la primera vez que se ejecuta.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a SQLite. El archivo se guarda en la raíz del proyecto.
SQLALCHEMY_DATABASE_URL = "sqlite:///./citas_medicas.db"

# El parámetro check_same_thread=False es necesario solo para SQLite,
# ya que permite que la conexión sea usada por más de un hilo (FastAPI).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal es la "fábrica" de sesiones. Cada petición HTTP usará una
# sesión independiente para comunicarse con la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que heredarán todos los modelos (tablas).
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI que entrega una sesión de base de datos.

    Se asegura de cerrar la sesión al finalizar la petición, incluso si
    ocurre algún error, evitando fugas de conexiones.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

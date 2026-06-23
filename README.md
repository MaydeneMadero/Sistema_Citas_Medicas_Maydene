# Sistema de Gestión de Citas Médicas y Automatización de Caja Contable

## 1. Nombre del proyecto
**Sistema de Gestión de Citas Médicas y Automatización de Caja Contable** (Backend).

## 2. Descripción general
Backend completo y funcional para administrar pacientes, médicos, citas médicas,
consultas, certificados médicos y reportes básicos. El proyecto está construido con
**FastAPI** y sigue una arquitectura por capas
**Modelo / Repositorio / Servicio / Controlador**, lo que mantiene el código ordenado,
legible y fácil de mantener. La documentación interactiva se genera automáticamente
mediante **Swagger/OpenAPI**.

## 3. Tecnologías utilizadas
- **Lenguaje:** Python 3.10+
- **Framework:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM:** SQLAlchemy
- **Base de datos:** SQLite (archivo local `citas_medicas.db`)
- **Validación de datos:** Pydantic
- **Documentación:** Swagger / OpenAPI (incluido en FastAPI)
- **Editor recomendado:** Visual Studio Code

## 4. Estructura del proyecto
```
citas_medicas_backend/
│
├── main.py                # Punto de entrada, registra routers y crea tablas
├── database.py            # Configuración de SQLAlchemy + SQLite
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Este documento
│
├── models/                # Modelos (tablas de la base de datos)
│   ├── paciente_model.py
│   ├── medico_model.py
│   ├── cita_model.py
│   ├── consulta_model.py
│   └── certificado_model.py
│
├── schemas/               # Esquemas Pydantic (validación de entrada/salida)
│   ├── paciente_schema.py
│   ├── medico_schema.py
│   ├── cita_schema.py
│   ├── consulta_schema.py
│   └── certificado_schema.py
│
├── repositories/          # Acceso a datos (consultas a la base de datos)
│   ├── paciente_repository.py
│   ├── medico_repository.py
│   ├── cita_repository.py
│   ├── consulta_repository.py
│   └── certificado_repository.py
│
├── services/              # Reglas de negocio y validaciones
│   ├── paciente_service.py
│   ├── medico_service.py
│   ├── cita_service.py
│   ├── consulta_service.py
│   └── certificado_service.py
│
└── controllers/           # Rutas / endpoints REST
    ├── paciente_controller.py
    ├── medico_controller.py
    ├── cita_controller.py
    ├── consulta_controller.py
    ├── certificado_controller.py
    └── reporte_controller.py
```

## 5. Instalación
1. Tener instalado **Python 3.10 o superior**.
2. Abrir la carpeta `citas_medicas_backend` en Visual Studio Code.
3. (Recomendado) Crear y activar un entorno virtual:

   **Windows (PowerShell):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 6. Ejecución en Visual Studio Code
1. Abrir la terminal integrada de VS Code (menú **Terminal → New Terminal**).
2. Asegurarse de estar dentro de la carpeta `citas_medicas_backend`.
3. Ejecutar el servidor:
   ```bash
   uvicorn main:app --reload
   ```
4. Al iniciar, se crea automáticamente el archivo de base de datos `citas_medicas.db`
   y todas sus tablas.

## 7. Acceso a Swagger
Con el servidor en ejecución, abrir en el navegador:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **Redoc:** http://127.0.0.1:8000/redoc
- **Estado del API:** http://127.0.0.1:8000/

## 8. Endpoints principales

### Pacientes
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/api/pacientes` | Crear paciente |
| GET    | `/api/pacientes` | Listar pacientes |
| GET    | `/api/pacientes/{id}` | Obtener paciente por id |
| PUT    | `/api/pacientes/{id}` | Actualizar paciente |
| DELETE | `/api/pacientes/{id}` | Eliminar paciente |

### Médicos
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/api/medicos` | Crear médico |
| GET    | `/api/medicos` | Listar médicos |
| GET    | `/api/medicos/{id}` | Obtener médico por id |
| PUT    | `/api/medicos/{id}` | Actualizar médico |
| DELETE | `/api/medicos/{id}` | Eliminar médico |

### Citas
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/api/citas` | Crear cita (estado inicial PENDIENTE) |
| GET    | `/api/citas` | Listar citas |
| GET    | `/api/citas/{id}` | Obtener cita por id |
| PUT    | `/api/citas/{id}` | Actualizar cita |
| DELETE | `/api/citas/{id}` | Eliminar cita |
| GET    | `/api/citas/paciente/{cedula}` | Citas de un paciente por cédula |

### Consultas
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/api/consultas` | Registrar consulta (la cita debe existir) |
| GET    | `/api/consultas` | Listar consultas |
| GET    | `/api/consultas/{id}` | Obtener consulta por id |
| GET    | `/api/consultas/paciente/{cedula}` | Consultas por cédula |

### Certificados
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST   | `/api/certificados` | Emitir certificado |
| GET    | `/api/certificados` | Listar certificados |
| GET    | `/api/certificados/{id}` | Obtener certificado por id |
| GET    | `/api/certificados/paciente/{cedula}` | Certificados por cédula |

### Reportes
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/api/reportes/historia-clinica/{cedula}` | Historia clínica completa |
| GET    | `/api/reportes/resumen-citas` | Resumen de citas por estado |
| GET    | `/api/reportes/citas-por-estado/{estado}` | Citas filtradas por estado |

## Reglas funcionales implementadas
1. No se crea una cita si el paciente no existe.
2. No se crea una cita si el médico no existe.
3. El estado inicial de una cita es **PENDIENTE**.
4. Una cita solo puede estar en **PENDIENTE**, **ATENDIDA** o **CANCELADA**.
5. Para registrar una consulta, la cita debe existir (la cita pasa a **ATENDIDA**).
6. `/api/citas/paciente/{cedula}` permite consultar las citas por cédula.
7. La historia clínica devuelve datos del paciente, citas atendidas, consultas,
   diagnósticos, tratamientos y certificados.

## 9. Evidencias sugeridas para capturas (PDF final)
1. Estructura del proyecto en el explorador de VS Code.
2. Terminal mostrando `uvicorn main:app --reload` en ejecución.
3. Página principal de Swagger (`/docs`) con todos los módulos.
4. Creación de un paciente (POST) con su respuesta JSON.
5. Creación de un médico (POST) con su respuesta JSON.
6. Creación de una cita (POST) mostrando estado `PENDIENTE`.
7. Error al crear una cita con paciente o médico inexistente.
8. Registro de una consulta y cómo la cita cambia a `ATENDIDA`.
9. Emisión de un certificado médico.
10. Reporte de historia clínica por cédula.
11. Reporte de resumen de citas por estado.
12. Archivo `citas_medicas.db` creado automáticamente.

## 10. Autor
**Maydene Alejandra Madero Lascano**

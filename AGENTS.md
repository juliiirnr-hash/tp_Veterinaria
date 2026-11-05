# Instrucciones y Contexto para Agentes y Desarrolladores (`AGENTS.md`)

Este documento establece las directrices arquitectónicas, reglas de negocio y restricciones técnicas para el desarrollo, mantenimiento y revisión de código en el proyecto **API Veterinaria (Programación III - UTN)**.

---

## 🏗️ 1. Arquitectura y Estructura del Proyecto

El proyecto sigue una organización estricta por **módulos funcionales**. Cada módulo es independiente y encapsula sus propias responsabilidades:

* **Módulos obligatorios**: `health`, `duenios`, `mascotas`, `practicas`, `turnos`, `laboratorio`.
* **Ubicación de entidades específicas**:
  * `FichaDuenio` vive dentro del módulo `duenios`.
  * `TurnoPractica` (tabla intermedia) vive dentro del módulo `turnos`.
* **Estructura interna por módulo**:
  * `models.py`: Modelos de tabla SQLModel, restricciones (`UNIQUE`, `CHECK`), índices y relaciones bidireccionales (`Relationship(back_populates=...)`).
  * `schemas.py`: DTOs de entrada (`Create`, `Update`) y de salida (`Read`) separados de los modelos de tabla.
  * `service.py`: Lógica de negocio, traducción de errores de base de datos a códigos HTTP, y consultas con carga anticipada.
  * `router.py`: Endpoints de FastAPI (`async def`), inyección de dependencias y declaración de códigos de respuesta.

---

## ⚙️ 2. Reglas Técnicas y Tecnologías

* **Stack principal**: Python 3.12+, FastAPI, SQLModel 0.0.24+, SQLAlchemy 2.0 (asincrónico), asyncpg, PostgreSQL 16.
* **Ciclo de vida y Conexión**:
  * El motor asincrónico (`create_async_engine`) y la fábrica de sesiones se inicializan en el *lifespan* (`app/main.py`), se almacenan en `app.state` y el motor se cierra al apagar.
  * Cada handler recibe la sesión mediante `Depends(get_session)` (una por petición) configurada con `expire_on_commit=False`.
* **Manejo de Dinero**: 
  * Todo monto monetario (`precio`, `precio_unitario`, `total`) se representa estrictamente con `Decimal`, **nunca** con `float`.
* **Asincronía**:
  * Todos los handlers (`router.py`) deben ser `async def`.
  * Ninguna operación bloqueante (como llamadas de terceros sincrónicas) debe ejecutarse de forma directa bloqueando el bucle de eventos principal.

---

## 🛡️ 3. Manejo de Integridad y Reglas de Negocio (RN-01 a RN-09)

* **Cero validaciones previas de existencia**: No se deben realizar consultas previas del tipo *"¿ya existe?"* antes de insertar o actualizar, para evitar condiciones de carrera.
* **Captura de excepciones**: Las operaciones de escritura deben delegar las restricciones a la base de datos (`UNIQUE`, `CHECK`, claves foráneas). Si la base rechaza la operación, el `service` debe capturar `IntegrityError`, realizar un *rollback* de la transacción y responder con un código **`409 Conflict`** y un mensaje descriptivo.
* **Borrados en cascada y restricciones**:
  * Dueño con mascotas: `ON DELETE RESTRICT` (`409` si se intenta borrar un dueño con mascotas).
  * Turno con prácticas: `ON DELETE CASCADE` manejado directamente por la base de datos (`passive_deletes=True` en la relación del ORM).

---

## 🔍 4. Optimización de Lecturas (Sin Problema $N+1$)

* Toda respuesta que incluya datos relacionados debe utilizar **carga anticipada declarada en la misma consulta**:
  * `joinedload` para relaciones a uno (ej. `Dueño.ficha`, `Mascota.duenio`, `Turno.mascota`).
  * `selectinload` para colecciones (ej. `Dueño.mascotas`, `Turno.practicas`).
* Las consultas deben resolverse en un **número fijo de queries** independiente de la cantidad de elementos asociados, evitando excepciones de tipo `MissingGreenlet`.

---

## 🧪 5. Validación y Pruebas

* Toda modificación o adición de código debe respetar los códigos de respuesta HTTP esperados:
  * `201`: Creación exitosa.
  * `204`: Borrado exitoso (sin cuerpo).
  * `400 / 404`: Recurso no encontrado.
  * `409`: Conflicto por violación de restricciones de base de datos.
  * `422`: Error de validación de esquemas (DTOs / parámetros inválidos).
* Las pruebas se validan ejecutando el script `python reiniciar.py` y utilizando los archivos `.http` ubicados en la carpeta `test/`.
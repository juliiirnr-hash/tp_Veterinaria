# API Veterinaria - Programación III (UTN)

Proyecto desarrollado para la materia **Programación III** de la **Tecnicatura Universitaria en Programación (UTN)**. Consiste en una API asincrónica construida con **FastAPI**, **SQLModel**, **SQLAlchemy (asincrónico)** y **PostgreSQL**, que implementa un sistema de gestión para una veterinaria de barrio (dueños, fichas, mascotas, prácticas y turnos).

---

## 🛠️ Requisitos Técnicos

* **Python**: 3.12 o superior
* **PostgreSQL**: Versión 16
* **FastAPI** (con standard) y dependencias listadas en `requirements.txt`

---

## 🚀 Instrucciones de Instalación y Puesta en Marcha

Sigue estos pasos para levantar el proyecto desde cero en tu entorno local:

### 1. Clonar el repositorio e ingresar a la carpeta
```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows (Command Prompt o PowerShell):
venv\Scripts\activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
Crea un archivo `.env` en la raíz del proyecto basándote en el archivo de ejemplo `env.example`:
```bash
# Linux/macOS
cp env.example .env
# Windows (CMD)
copy env.example .env
```
Edita el archivo `.env` y asegúrate de configurar correctamente la cadena de conexión a tu base de datos PostgreSQL (utilizando el driver `asyncpg`):
```env
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/nombre_base_datos
```

### 5. Crear la base vacía en PostgreSQL
El script `reiniciar.py` crea las tablas, pero no la base. Creala una sola vez (si ya existe, saltá este paso):
```bash
createdb -U postgres -h localhost veterinaria
```
También podés crearla desde pgAdmin con el nombre `veterinaria`.

### 6. Inicializar la base de datos y cargar datos iniciales
Ejecuta el script de reinicio para borrar las tablas existentes (si las hubiera), crearlas mediante `SQLModel.metadata.create_all` y poblar los datos iniciales obligatorios:
```bash
python reiniciar.py
```

### 7. Ejecutar el servidor de desarrollo
Inicia la aplicación utilizando `uvicorn`:
```bash
uvicorn app.main:app --reload
```
La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

---

## 🧪 Pruebas y Casos de Uso (`test/`)
En la carpeta `test/` encontrarás archivos de pruebas con peticiones HTTP (`.http`) orientadas a verificar los distintos casos de negocio (C-01 al C-09), manejo de códigos de error (`404`, `409`, `422`), validaciones de restricciones en la base de datos y la concurrencia asincrónica.

Los casos se ejecutan **después de `python reiniciar.py`**, que deja la base en el estado conocido que esperan los archivos (por ejemplo, el turno 1 con dos prácticas y los ids iniciales).

* `00_health.http` a `05_laboratorio.http`: casos C-01 a C-09.
* `04_check_practica.sql`: C-08, ejecutado con `psql`; la base rechaza `UPDATE practica SET precio = 0` por el `CHECK`.
* `c05_cascada.sql`: C-05, verifica con `psql` que el turno borrado no dejó filas en `turno_practica`.
* `c09_concurrencia.py`: C-09 automatizado; lanza tres consultas al laboratorio y un `GET /health/live` en paralelo. Se ejecuta con `.venv\Scripts\python.exe test\c09_concurrencia.py`.

---

## 🔍 Evidencia C-07: Consultas Fijas (`echo=True`)

`echo=True` está activo en `app/core/database.py`, así que cada sentencia que llega a la base se imprime en la consola. El detalle de un turno emite siempre **3 consultas**, sin importar cuántas prácticas tenga:

1. `SELECT turno ... LEFT OUTER JOIN mascota` — `joinedload(Turno.mascota)`.
2. `SELECT turno_practica ... WHERE turno_id IN (...)` — `selectinload(Turno.practicas)`.
3. `SELECT practica ... WHERE id IN (...)` — `selectinload(TurnoPractica.practica)`.

Salida real capturada con `uvicorn` y PostgreSQL (el log de SQLAlchemy muestra los parámetros con `$1`, `$2`, ...):

```sql
-- turno con 1 práctica
SELECT turno.id, turno.mascota_id, turno.fecha, turno.motivo, turno.total, mascota_1.id AS id_1, mascota_1.nombre, mascota_1.especie, mascota_1.duenio_id
FROM turno LEFT OUTER JOIN mascota AS mascota_1 ON mascota_1.id = turno.mascota_id
WHERE turno.id = $1::INTEGER
SELECT turno_practica.turno_id, turno_practica.practica_id, turno_practica.precio_unitario
FROM turno_practica
WHERE turno_practica.turno_id IN ($1::INTEGER)
SELECT practica.id, practica.nombre, practica.precio
FROM practica
WHERE practica.id IN ($1::INTEGER)

-- turno con 3 prácticas: las mismas 3 consultas; sólo crece el IN
SELECT turno.id, turno.mascota_id, turno.fecha, turno.motivo, turno.total, mascota_1.id AS id_1, mascota_1.nombre, mascota_1.especie, mascota_1.duenio_id
FROM turno LEFT OUTER JOIN mascota AS mascota_1 ON mascota_1.id = turno.mascota_id
WHERE turno.id = $1::INTEGER
SELECT turno_practica.turno_id, turno_practica.practica_id, turno_practica.precio_unitario
FROM turno_practica
WHERE turno_practica.turno_id IN ($1::INTEGER)
SELECT practica.id, practica.nombre, practica.precio
FROM practica
WHERE practica.id IN ($1::INTEGER, $2::INTEGER, $3::INTEGER)
```

| Lectura | Consultas |
|---|---|
| Detalle de turno con 1 práctica | 3 |
| Detalle de turno con 3 prácticas | 3 |
| Dueño con su ficha | 1 |
| Mascota con su dueño | 1 |
| Dueño con sus mascotas | 2 |

Los casos C-07 de `test/03_lecturas_paginacion_borrados.http` crean un turno con una práctica y otro con tres para comparar la salida en la consola.

---

## 💡 Explicación Técnica: Índice de Claves Foráneas en `turno_practica`

Como se detalla en el modelo de dominio, PostgreSQL no crea de forma automática índices para las claves foráneas, por lo que deben solicitarse explícitamente en la definición de las tablas. Sin embargo, existe una excepción en este diseño:

* **¿Por qué `turno_practica.turno_id` no lleva un índice propio?**
  La tabla intermedia `turno_practica` posee una **clave primaria compuesta** definida como `(turno_id, practica_id)`. En motores relacionales como PostgreSQL, un índice B-tree sobre una clave primaria compuesta indexa las columnas en el orden estricto en que fueron declaradas. Dado que `turno_id` ocupa la **primera posición** de la clave primaria, el índice primario ya cubre de manera óptima cualquier consulta o filtro que busque por `turno_id` (por ejemplo, al hacer un `JOIN` o un borrado en cascada), haciendo que un índice independiente sobre ese campo sea redundante e innecesario.

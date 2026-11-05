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
cp env.example .env
```
Edita el archivo `.env` y asegúrate de configurar correctamente la cadena de conexión a tu base de datos PostgreSQL (utilizando el driver `asyncpg`):
```env
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/nombre_base_datos
```

### 5. Inicializar la base de datos y cargar datos iniciales
Ejecuta el script de reinicio para borrar las tablas existentes (si las hubiera), crearlas mediante `SQLModel.metadata.create_all` y poblar los datos iniciales obligatorios:
```bash
python reiniciar.py
```

### 6. Ejecutar el servidor de desarrollo
Inicia la aplicación utilizando `uvicorn`:
```bash
uvicorn app.main:app --reload
```
La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

---

## 🧪 Pruebas y Casos de Uso (`test/`)
En la carpeta `test/` encontrarás archivos de pruebas con peticiones HTTP (`.http`) orientadas a verificar los distintos casos de negocio (C-01 al C-09), manejo de códigos de error (`404`, `409`, `422`), validaciones de restricciones en la base de datos y la concurrencia asincrónica.

---

## 💡 Explicación Técnica: Índice de Claves Foráneas en `turno_practica`

Como se detalla en el modelo de dominio, PostgreSQL no crea de forma automática índices para las claves foráneas, por lo que deben solicitarse explícitamente en la definición de las tablas. Sin embargo, existe una excepción en este diseño:

* **¿Por qué `turno_practica.turno_id` no lleva un índice propio?**
  La tabla intermedia `turno_practica` posee una **clave primaria compuesta** definida como `(turno_id, practica_id)`. En motores relacionales como PostgreSQL, un índice B-tree sobre una clave primaria compuesta indexa las columnas en el orden estricto en que fueron declaradas. Dado que `turno_id` ocupa la **primera posición** de la clave primaria, el índice primario ya cubre de manera óptima cualquier consulta o filtro que busque por `turno_id` (por ejemplo, al hacer un `JOIN` o un borrado en cascada), haciendo que un índice independiente sobre ese campo sea redundante e innecesario.
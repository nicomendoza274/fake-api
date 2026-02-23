# Fake-API

Welcome to the Fake-API repository! This is a simple guide to help you get started with setting up and running the Fake-API project.

## Actual version

The actual version is [v2.1.0](https://github.com/nicomendoza274/fake-api/releases/tag/v2.1.0).

## Getting Started

- **Clone the repository:**

  ```sh
  git clone git@github.com:nicomendoza274/fake-api.git
  cd fake-api
  ```

## Installation

Elige una de las siguientes opciones según la herramienta que quieras usar: **Virtualenv**, **UV** o **Docker**.

---

### Opción 1: Virtualenv

Requisitos: **Python 3.13+**

1. **Crear y activar el entorno virtual**

   macOS/Linux:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Windows:

   ```sh
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Instalar dependencias**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**

   Copia el ejemplo y crea tus archivos de entorno (por ejemplo `.env.dev`, `.env.qa`, `.env.prod`):

   ```sh
   cp env.example .env.dev
   ```

   Edita el archivo y configura las variables (base de datos, secretos, etc.).

4. **Ejecutar el proyecto**

   Desarrollo:

   ```sh
   uvicorn src.main:app --env-file .env.dev --reload
   ```

   QA:

   ```sh
   uvicorn src.main:app --env-file .env.qa --reload
   ```

   También puedes usar el **perfil del debugger** en VS Code y pulsar **F5** (por defecto usa QA).

---

### Opción 2: UV

Requisitos: [UV](https://docs.astral.sh/uv/) instalado y **Python 3.13+**.

1. **Crear y activar el entorno virtual con UV**

   ```sh
   uv python install 3.13
   uv venv
   ```

2. **Instalar dependencias**

   ```sh
   uv sync
   ```

3. **Configurar variables de entorno**

   ```sh
   cp env.example .env.dev
   ```

   Edita `.env.dev` con tu configuración.

4. **Ejecutar el proyecto**

   Desarrollo:

   ```sh
   uv run uvicorn src.main:app --env-file .env.dev --reload
   ```

   QA:

   ```sh
   uv run uvicorn src.main:app --env-file .env.qa --reload
   ```

---

### Opción 3: Docker

Requisitos: **Docker** y **Docker Compose**.

La API y PostgreSQL se levantan con Docker Compose. No necesitas instalar Python ni dependencias en tu máquina.

1. **Configurar variables de entorno**

   Crea un archivo `.env` en la raíz del proyecto (o copia desde `env.example`):

   ```sh
   cp env.example .env
   ```

   Ajusta al menos `DB_NAME`, `DB_USER` y `DB_PASSWORD` si quieres valores distintos a los por defecto (`fake_api_db`, `postgres`, `password`). Con Docker, `DB_HOST` debe ser `db` (ya viene definido en el compose).

2. **Levantar los servicios**

   ```sh
   docker compose up --build
   ```

   Para ejecutar en segundo plano:

   ```sh
   docker compose up -d --build
   ```

3. **Acceder a la API**
   - API: [http://localhost:8000](http://localhost:8000)
   - Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
   - PostgreSQL: `localhost:5432` (usuario y base según tu `.env`)

4. **Detener los servicios**

   ```sh
   docker compose down
   ```

   Para eliminar también el volumen de la base de datos:

   ```sh
   docker compose down -v
   ```

---

Una vez el proyecto esté en marcha (con cualquiera de las opciones), puedes abrir [http://localhost:8000](http://localhost:8000) en el navegador.

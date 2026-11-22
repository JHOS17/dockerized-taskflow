# Dockerized TaskFlow

API REST construida con **FastAPI** conectada a **PostgreSQL 16** y expuesta mediante **Nginx** como *reverse proxy*, orquestada con **Docker Compose** y configurada con réplicas del servicio de API y gestión de secretos.

## Arquitectura

* **`nginx` (`nginx:1.27-alpine`):** Escucha en el puerto `80` del host y reenvía las peticiones (`proxy_pass`) hacia el bloque `upstream` de la API, conservando las cabeceras originales del cliente.
* **`api` (FastAPI + Uvicorn + SQLAlchemy):** Servicio backend en la red interna de Docker (`8000/tcp`), configurado con réplicas (`deploy.replicas: 2`) y conectado a PostgreSQL.
* **`db` (`postgres:16-alpine`):** Base de datos relacional con volumen persistente (`postgres_data`) y *healthcheck* (`pg_isready`) para asegurar que esté lista antes de iniciar la API.

## Estructura del proyecto

```text
dockerized-taskflow/
├── app/
│   ├── database.py
│   ├── main.py
│   └── models.py
├── nginx/
│   └── nginx.conf
├── secrets/
│   └── db_password.txt
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Requisitos previos

* Docker y Docker Compose instalados.
* Archivo `secrets/db_password.txt` creado con la contraseña de la base de datos (asegúrate de tenerlo en `.gitignore` si vas a subir el repositorio).

## Cómo ejecutar el proyecto

1. **Detén cualquier servicio Nginx externo que ocupe el puerto `80`** (por ejemplo, si usas Ubuntu/WSL):

   ```bash
   sudo systemctl stop nginx
   ```

2. **Construye y levanta los servicios en segundo plano:**

   ```bash
   docker compose up -d --build
   ```

3. **Verifica el estado de los contenedores:**

   ```bash
   docker compose ps
   ```

## Probar la aplicación

* Endpoint principal: `http://localhost/`
* Documentación interactiva (Swagger UI): `http://localhost/docs`

Ejemplo rápido con `curl`:

```bash
curl -i http://localhost/
curl -i http://localhost/docs
```

## Escalar réplicas y recargar Nginx

Si modificas el número de réplicas en `docker-compose.yml` o escalas desde la línea de comandos:

```bash
docker compose up -d --build --scale api=3
docker compose restart nginx
```

Para detener el stack:

```bash
docker compose down
```
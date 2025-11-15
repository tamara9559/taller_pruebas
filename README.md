1. Introducción al Proyecto

Eventia es un sistema backend diseñado para gestionar eventos, participantes y asistencias.
Su objetivo es ofrecer una API eficiente, escalable y fácil de mantener, permitiendo:

-Registrar eventos y participantes
-Controlar capacidad de eventos
-Registrar asistencias
-Obtener estadísticas de ocupación
-Mejorar el rendimiento mediante cache en Redis
-Garantizar calidad mediante pruebas automáticas

Además, el proyecto está completamente automatizado con un pipeline CI/CD basado en GitHub Actions, que ejecuta pruebas en cada push para asegurar la estabilidad del código.

2. Arquitectura Utilizada y Explicación

El proyecto adopta una arquitectura modular y basada en capas, siguiendo buenas prácticas de separación de responsabilidades:

2.1 Capas del sistema
Capa	Descripción
Controladores	Definen las rutas FastAPI y manejan las solicitudes HTTP.
Servicios	Contienen la lógica de negocio (validaciones, flujos, reglas).
Repositorios Acceden a la base de datos usando SQLAlchemy ORM.
Modelos	Representan tablas de BD con SQLAlchemy.
Infraestructura	Base de datos, Redis, variables de entorno.

2.2  "Clean Architecture" simplificada

Los controladores NO acceden directamente a la BD
Los servicios NO conocen detalles del framework web
Los repositorios NO contienen lógica de negocio

Esto permite:

Facilidad para hacer pruebas unitarias
Sustituir Redis o la base de datos sin afectar la lógica
Reducir acoplamiento

2.3 Cache con Redis

Redis se usa para optimizar consultas frecuentes:
Lista de eventos
Lista de participantes
Asistencias por evento
Estadísticas de ocupación

Cada cambio invalida el cache automáticamente.

3. Requisitos
Requisitos del sistema

Python 3.10+
Redis instalado (opcional para ejecución local)
MySQL o SQLite (depende de configuración)

Requisitos de Python

El archivo requirements.txt contiene:
fastapi
uvicorn
sqlalchemy
pymysql o sqlite
redis
pytest
python-dotenv

4. Instalación

1️ Clonar el repositorio:

git clone https://github.com/tamara9559/taller_pruebas.git
cd taller_pruebas/eventia


2️ Crear entorno virtual:

python -m venv venv


3️ Activarlo:

Windows:
venv\Scripts\activate


4️ Instalar dependencias:

pip install -r requirements.txt


5️ Crear archivo .env:

ENV=local
DATABASE_URL=sqlite:///./eventia.db
REDIS_HOST=localhost
REDIS_PORT=6379

5. Ejecución en Local

Iniciar servidor FastAPI:
uvicorn app.main:app --reload

Endpoints utilitarios:
Docs Swagger:
http://127.0.0.1:8000/docs

6. Ejecución de Pruebas

Ejecutar todas las pruebas:
pytest -v


Ejecutar solo pruebas unitarias:
pytest eventia/test/unit


El pipeline ejecuta exactamente este comando:
pytest eventia/test/unit --maxfail=1 --disable-warnings

7. Explicación del Pipeline (GitHub Actions)

El pipeline CI/CD es ejecutado automáticamente en cada:
push
pull request hacia main

El pipeline hace:

1️ Instala Python
2️ Instala dependencias
3️ Configura variables de entorno ENV=TEST
4️ Ejecuta pruebas unitarias
5️ Reporta fallos en GitHub

8. Justificación de Tecnologías Elegidas
FastAPI

Rápido, moderno y con excelente rendimiento
Validación automática con Pydantic
Documentación automática con Swagger

SQLAlchemy

ORM robusto
Permite cambiar entre MySQL, PostgreSQL, SQLite sin modificar código

 Redis

Cache en memoria ultrarrápido
Reduce carga de base de datos
Ideal para estadísticas y listados grandes

Pytest

Simple y poderoso para pruebas unitarias
Permite fixtures como DB en memoria o mocks de Redis






hecho por juan diego támara escobar

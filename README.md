# 🐳 Docker Demo — Versioned FastAPI REST API

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="48" alt="Python" />
  &nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="48" alt="FastAPI" />
  &nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="48" alt="PostgreSQL" />
  &nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="48" alt="Docker" />
</p>

<p align="center">
  <strong>A containerized REST API built with FastAPI, PostgreSQL, SQLAlchemy ORM, and Docker Compose.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/ORM-SQLAlchemy-D71F00" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/Container-Docker-2496ED?logo=docker" alt="Docker" />
</p>

---

## 📌 Overview

**Docker Demo** is a backend project demonstrating how to build, organize, version, and containerize RESTful APIs using modern Python technologies.

The project provides APIs for user and task management, integrates PostgreSQL for data persistence, and uses SQLAlchemy ORM to interact with the database. Docker and Docker Compose simplify application setup and deployment.

## ✨ Key Features

- 🚀 **FastAPI Framework** — Build high-performance REST APIs.
- 🔢 **API Versioning** — Organize endpoints into V1, V2, and V3.
- 👤 **User Management** — Create, retrieve, update, and delete users.
- ✅ **Task Management** — Manage tasks and associate them with users.
- 🗄️ **PostgreSQL Database** — Store application data in a relational database.
- 🔗 **SQLAlchemy ORM** — Work with database records using Python objects.
- 🐳 **Docker Support** — Package the application into a container.
- ⚙️ **Docker Compose** — Simplify application startup and service configuration.
- 📖 **Interactive API Docs** — Explore endpoints through Swagger UI and ReDoc.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming language |
| ⚡ FastAPI | REST API framework |
| 🗄️ PostgreSQL | Relational database |
| 🔗 SQLAlchemy | Object-relational mapping |
| 📦 Pydantic | Data validation |
| 🦄 Uvicorn | ASGI application server |
| 🐳 Docker | Application containerization |
| ⚙️ Docker Compose | Container orchestration |

## 📂 Project Structure

```text
Docker-demo/
├── README.md
├── requirements.txt
├── .gitignore
│
├── Docker/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker.md
│   └── docker_demo.py
│
├── Postman/
│   ├── PMS Task Manager API.postman_collection.json
│   ├── v1/
│   │   ├── Health management api.postman_collection.json
│   │   └── Screenshot 2026-11-03 161531.png
│   └── v2/
│       ├── Health management api with data validation and error message.postman_collection.json
│       └── error_messages/
│           ├── Screenshot 2026-11-05 154151.png
│           ├── Screenshot 2026-11-05 154224.png
│           ├── Screenshot 2026-11-05 154258.png
│           ├── Screenshot 2026-11-05 154935.png
│           └── Screenshot 2026-11-05 161015.png
│
├── fastapi_endpoint/
│   │
│   ├── main.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── fastapi_arch_v1.md
│   │   ├── fastapi_arch_v2.md
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       └── users.py
│   │   ├── v2/
│   │   │   └── endpoints/
│   │   │       └── users.py
│   │   └── v3/
│   │       └── endpoints/
│   │           ├── tasks.py
│   │           └── users.py
│   │
│   └── models/
│       └── users.py
│
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## API Endpoint

**GET /health**

- Default endpint : 
```text 
http://localhost:8000/health
```
- Version 1 endpoint : 
```text 
http://localhost:8000/api/v1/
```
- Version 2 endpoint : 
```text 
http://localhost:8000/api/v2/
```


## Technologies Used

- Python 3.10
- Pydantic
- FastAPI
- Uvicorn
- Docker
- Docker Compose

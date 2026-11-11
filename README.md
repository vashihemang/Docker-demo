# 🐳 Docker Demo — FastAPI REST API

<p align="center">
  <strong>A versioned REST API built with FastAPI, PostgreSQL, SQLAlchemy, and Docker.</strong>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python 3.10">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white" alt="Docker">
  </a>
  <a href="https://docs.pytest.org">
    <img src="https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  </a>
</p>

---

## 📌 Overview

**Docker Demo** is a Python backend project that demonstrates REST API development, API versioning, database integration, and containerization.

Built with FastAPI and PostgreSQL, the project organizes API endpoints into multiple versions and demonstrates user and task management operations. Docker and Docker Compose provide a convenient way to build and run the application.

## ✨ Features

- ⚡ **FastAPI** — Modern framework for building RESTful APIs.
- 🔢 **API Versioning** — Separate API versions: V1, V2, and V3.
- 👤 **User Management** — CRUD operations for user resources.
- ✅ **Task Management** — Task operations and user-task relationships.
- 🗄️ **PostgreSQL** — Relational database integration.
- 🔗 **SQLAlchemy ORM** — Database interaction through Python models.
- 🐳 **Docker** — Containerized application environment.
- ⚙️ **Docker Compose** — Simplified container startup and management.
- 📖 **Interactive Documentation** — Explore endpoints using Swagger UI.
- 🧪 **Postman Resources** — API testing resources included in the repository.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python 3.10 | Backend development |
| ⚡ FastAPI | REST API framework |
| 🗄️ PostgreSQL | Relational database |
| 🔗 SQLAlchemy | Object-relational mapping |
| 📋 Pydantic | Data validation |
| 🚀 Uvicorn | ASGI application server |
| 🐳 Docker | Containerization |
| ⚙️ Docker Compose | Container orchestration |
| 🧪 Postman | API testing |

## 📂 Project Structure

```text
Docker-demo/
├── .gitignore
├── README.md                 
├── requirements.txt
├── Docker/
│   ├── .dockerignore
│   ├── docker-compose.yml
│   ├── docker.md
│   ├── Dockerfile
│   └── docker_demo.py
├── fastapi_endpoints/
│   ├── .env
│   ├── alembic.ini
│   ├── main.py
│   ├── alembic/
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 0053c30eda7c_create_users_tasks_sessions.py
│   │       └── e0624a62042b_add_work_notes_to_tasks.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── fastapi_arch_v1.md
│   │   ├── fastapi_arch_v2.md
│   │   ├── v1/endpoints/users.py
│   │   ├── v2/endpoints/users.py
│   │   └── v3/endpoints/
│   │       ├── tasks.py
│   │       └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── users_v3.py
│   ├── scripts/
│   │   └── seed_users.py
│   └── tests/
│       ├── conftest.py
│       └── test_auth_tasks.py
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
└── .pytest_cache/             (generated test cache)
```

*Directory overview is based on the repository's documented structure. Verify exact filenames against the branch you use.*

## 🚀 Getting Started

### Prerequisites

Make sure the following tools are installed:

- Python 3.10
- Docker Desktop or Docker Engine
- Docker Compose
- Git
- PostgreSQL, if running the application outside Docker

### 1. Clone the Repository

```bash
git clone https://github.com/vashihemang/Docker-demo.git
cd Docker-demo
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

Activate the environment on Windows:

```powershell
myenv\Scripts\activate
```

Activate the environment on Linux or macOS:

```bash
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the Database

Configure the database connection using the environment variable expected by the application.

Example PostgreSQL connection URL:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/docker_demo
```

Replace `YOUR_PASSWORD` with your local database password and create the `docker_demo` database if it does not already exist.

> 🔐 Never commit real credentials or secret environment variables to GitHub.

### 5. Start the Application

If the FastAPI application object is defined in `fastapi_endpoint/main.py`, run:

```bash
uvicorn fastapi_endpoint.main:app --reload
```

The API should be available at:

- **Base URL:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

The database must be configured and accessible before database-backed endpoints can work.

## 🐳 Run with Docker

Docker is the recommended option for a reproducible development environment.

### Build and Start

From the repository root:

```bash
docker compose up --build
```

To run containers in the background:

```bash
docker compose up --build -d
```

### Manage Containers

Check service status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop the services:

```bash
docker compose down
```

Rebuild the application after changing its dependencies or Docker configuration:

```bash
docker compose up --build -d
```

> Ensure `docker-compose.yml` defines the required application and database services and the correct environment variables. The commands depend on the services configured in that file.

## 🔌 API Endpoints

The documented API design includes versioned user endpoints and task endpoints in V3.

### 👤 V1 — User APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users` | Retrieve users |
| `GET` | `/api/v1/users/{user_id}` | Retrieve a user by ID |
| `POST` | `/api/v1/users` | Create a user |
| `PUT` | `/api/v1/users/{user_id}` | Update a user |
| `DELETE` | `/api/v1/users/{user_id}` | Delete a user |

### 👤 V2 — User APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v2/users` | Retrieve users |
| `GET` | `/api/v2/users/{user_id}` | Retrieve a user by ID |
| `POST` | `/api/v2/users` | Create a user |
| `PUT` | `/api/v2/users/{user_id}` | Update a user |
| `PATCH` | `/api/v2/users/{user_id}` | Partially update a user |
| `DELETE` | `/api/v2/users/{user_id}` | Delete a user |

### 👤 V3 — User APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v3/users` | Retrieve users |
| `GET` | `/api/v3/users/{user_id}` | Retrieve a user by ID |
| `POST` | `/api/v3/users` | Create a user |
| `PUT` | `/api/v3/users/{user_id}` | Update a user |
| `PATCH` | `/api/v3/users/{user_id}` | Partially update a user |
| `DELETE` | `/api/v3/users/{user_id}` | Delete a user |
| `GET` | `/api/v3/users/{user_id}/tasks` | Retrieve tasks for a user |

### ✅ V3 — Task APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v3/tasks` | Retrieve tasks |
| `GET` | `/api/v3/tasks/{task_id}` | Retrieve a task by ID |
| `POST` | `/api/v3/tasks` | Create a task |
| `PUT` | `/api/v3/tasks/{task_id}` | Update a task |
| `PATCH` | `/api/v3/tasks/{task_id}` | Partially update a task |
| `DELETE` | `/api/v3/tasks/{task_id}` | Delete a task |

**Note:** Confirm these routes against the active branch and generated OpenAPI documentation. Actual route prefixes and supported methods may differ.

## 🗄️ Database Design

The project documentation describes two primary resources: users and tasks.

### Users

Typical fields:

- `id` — Unique identifier
- `name` — User name
- `email` — Email address
- `phone` — Contact number
- `status` — User status
- `created_at` — Creation timestamp

### Tasks

Typical fields:

- `id` — Unique task identifier
- `title` — Task title
- `description` — Task details
- `status` — Task status
- `user_id` — Associated user
- `created_at` — Creation timestamp

**Relationship:** One user can have multiple tasks, represented by a one-to-many relationship.

*Field names and relationships should be checked against the actual SQLAlchemy models.*

## 🧪 Testing the API

Use the Postman resources in the repository or the FastAPI-generated documentation to test the endpoints.

1. Start the application.
2. Open http://127.0.0.1:8000/docs.
3. Select an API endpoint.
4. Click **Try it out**.
5. Enter the required parameters and request body.
6. Execute the request and inspect the response.

For the documented health-check endpoint, try:

```bash
curl http://localhost:8000/health
```

This request assumes the application exposes `GET /health` on the mapped port.

## 🩺 Troubleshooting

| Problem | What to check |
|---|---|
| Docker daemon is unavailable | Start Docker Desktop or Docker Engine. |
| Container fails to start | Review `docker compose logs`. |
| Database connection error | Verify database credentials, hostname, port, and database name. |
| Port 8000 is occupied | Stop the conflicting service or change the port mapping. |
| Module import error | Check the application package path and virtual environment. |
| API documentation does not load | Verify the application is running and port 8000 is mapped correctly. |

## 🔒 Security Recommendations

- Keep database credentials outside source code.
- Exclude `.env` files from version control.
- Use least-privilege database accounts.
- Validate and sanitize incoming data.
- Configure authentication and authorization where required.
- Avoid exposing PostgreSQL ports publicly without a specific need.

## 🎯 Learning Objectives

This project is useful for learning:

- REST API development with FastAPI
- API versioning and modular route organization
- SQLAlchemy and PostgreSQL integration
- CRUD operations
- Docker image creation and container execution
- Multi-service development with Docker Compose
- Interactive API documentation and endpoint testing

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit with a descriptive message.
5. Open a pull request.


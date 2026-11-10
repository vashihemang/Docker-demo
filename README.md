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
├── fastapi_endpoints/
│   ├── .env
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
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
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── users_v3.py
│   │   └── __pycache__/
│   │
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── seed_users.py
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_auth_tasks.py
│       └── __pycache__/
│
└── .pytest_cache/
    ├── .gitignore
    ├── CACHEDIR.TAG
    ├── README.md
    └── v/
        └── cache/
```

> Note: The structure above is a simplified overview. Directory names and file locations should match the actual repository.

## ⚙️ Prerequisites

Before running the project, install:

- 🐍 Python 3.10 or a compatible version
- 🐳 Docker Desktop or Docker Engine
- ⚙️ Docker Compose
- 🔧 Git

For local execution without Docker, PostgreSQL must also be installed and configured.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/vashihemang/Docker-demo.git
cd Docker-demo
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

Activate it on Windows:

```powershell
myenv\Scripts\activate
```

On Linux or macOS:

```bash
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Configure your PostgreSQL connection using the environment variable expected by the application.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/docker_demo
```

Replace `YOUR_PASSWORD` with your PostgreSQL password and ensure the database exists.

> 🔐 Security: Never commit real database credentials, API keys, or other secrets to GitHub.

### 5. Run the Application Locally

From the repository root, activate the virtual environment and enter the FastAPI
application directory:

```powershell
.\myenv\Scripts\Activate.ps1
cd .\fastapi_endpoints
alembic upgrade head
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The application modules use imports relative to `fastapi_endpoints`, so run
Uvicorn from that directory.

Once the server starts, open:

- 🌐 API Base URL: http://127.0.0.1:8000
- 📘 Swagger UI: http://127.0.0.1:8000/docs
- 📖 ReDoc: http://127.0.0.1:8000/redoc

## 🗃️ Database Migrations

Alembic records and applies database schema changes (tables, columns, indexes)
as ordered migration files, so each environment can be upgraded consistently
without manually recreating its database. These task permission and endpoint
changes do not alter the schema, so no new migration is needed for them.

Set `DATABASE_URL` in `fastapi_endpoints/.env` to a PostgreSQL connection URL,
then run Alembic commands from `fastapi_endpoints`:

```bash
cd fastapi_endpoints
```

Apply all pending migrations (including the initial users, tasks, and sessions
tables and the `tasks.work_notes` column):

```bash
alembic upgrade head
```

After changing SQLAlchemy models, create a migration and review the generated file in `alembic/versions/` before applying it:

```bash
alembic revision --autogenerate -m "describe the schema change"
alembic upgrade head
```

Roll back the most recent migration and reapply it:

```bash
alembic downgrade -1
alembic upgrade head
```

Check the current revision and migration history:

```bash
alembic current
alembic history
```

For a database that already has these tables, compare its schema with the migrations first. Only if it exactly matches the target revision, mark it as migrated with `alembic stamp head`; this records the revision without changing table data or structure. Do not use `stamp` to skip unapplied schema changes.

## 🐳 Running with Docker

### Option 1: Docker Compose (Recommended)

Build the image and start the configured services:

```bash
docker compose up --build
```

Run services in the background:

```bash
docker compose up --build -d
```

View running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

Stop the services:

```bash
docker compose down
```

### Option 2: Build and Run a Docker Image

Build the application image:

```bash
docker build -t fastapi-demo .
```

Start the container:

```bash
docker run --rm -p 8000:8000 fastapi-demo
```

> 💡 The Dockerfile must configure the application entry point, and the container must expose the appropriate application port. Database connectivity must also be configured correctly.

## 🔌 API Endpoints

The project organizes its REST API into multiple versions.

### 🔐 Authentication

Teacher registration is protected by a private invite key. Set a random
`TEACHER_REGISTRATION_KEY` value (at least 32 characters) in
`fastapi_endpoints/.env`. Keep this value private and do not commit it.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/teacher/register` | Register a teacher; requires the `X-Teacher-Registration-Key` header |
| POST | `/auth/teacher/login` | Teacher login only |
| POST | `/auth/register` | Student registration |
| POST | `/auth/student/login` | Student login only |
| POST | `/auth/login` | Student or teacher login |
| GET | `/auth/me` | Get the authenticated user's profile |
| POST | `/auth/refresh` | Refresh access and refresh tokens |
| POST | `/auth/logout` | Log out the current session |

Teacher registration accepts the same JSON fields as student registration:
`name`, `email`, `password`, and optional `phone`. Teacher login accepts `email`
and `password`. Use the returned access token as a Bearer token for protected
endpoints.

### 👤 V1 — User Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/users` | Retrieve all users |
| GET | `/api/v1/users/{user_id}` | Retrieve a user by ID |
| POST | `/api/v1/users` | Create a user |
| PUT | `/api/v1/users/{user_id}` | Update a user |
| DELETE | `/api/v1/users/{user_id}` | Delete a user |

### 👤 V2 — User Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/users` | Retrieve all users |
| GET | `/api/v2/users/{user_id}` | Retrieve a user by ID |
| POST | `/api/v2/users` | Create a user |
| PUT | `/api/v2/users/{user_id}` | Update a user |
| PATCH | `/api/v2/users/{user_id}` | Partially update a user |
| DELETE | `/api/v2/users/{user_id}` | Delete a user |

### 👤 V3 — User Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v3/users` | Retrieve all users |
| GET | `/api/v3/users/{user_id}` | Retrieve a user by ID |
| POST | `/api/v3/users` | Create a user |
| PUT | `/api/v3/users/{user_id}` | Update a user |
| PATCH | `/api/v3/users/{user_id}` | Partially update a user |
| DELETE | `/api/v3/users/{user_id}` | Delete a user |
| GET | `/api/v3/users/{user_id}/tasks` | Retrieve a user's tasks |

### ✅ V3 — Task Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks/` | Student sees only own tasks; teacher sees all tasks |
| GET | `/tasks/{task_id}` | Get a task (student access is limited to own task) |
| POST | `/tasks/` | Teacher assigns a task; it must start as `pending` |
| PUT | `/tasks/{task_id}` | Student may set own task to `in_progress`/`done` and edit work notes; teacher may set status only to `pending` |
| GET | `/tasks/students` | Teacher sees each student's name and assigned tasks |
| GET | `/tasks/progress` | Teacher sees task progress counts |
| DELETE | `/tasks/{task_id}` | Teacher deletes a task |

## 🗄️ Database Design

The application uses PostgreSQL to store users and tasks.

### Users

Typical user fields include:

- `id` — Unique user identifier
- `name` — User's name
- `email` — User's email address
- `phone` — Contact number
- `status` — User status
- `created_at` — Record creation timestamp

### Tasks

Typical task fields include:

- `id` — Unique task identifier
- `title` — Task title
- `description` — Task details
- `status` — Current task status
- `user_id` — Associated user identifier
- `created_at` — Record creation timestamp

**Relationship:** One user can have multiple tasks (one-to-many relationship).

## 🧪 API Testing

Use the Postman resources included in the repository to test API requests.

You can also use the automatically generated Swagger UI:

1. Start the application.
2. Open http://127.0.0.1:8000/docs.
3. Select an endpoint.
4. Click **Try it out**.
5. Enter the required parameters or request body.
6. Execute the request and review the response.

## 🩺 Troubleshooting

| Issue | Suggested Solution |
|---|---|
| Docker is not running | Start Docker Desktop or the Docker Engine service. |
| Database connection fails | Verify the database URL, credentials, hostname, and port. |
| Port 8000 is already in use | Stop the conflicting process or configure another port. |
| Python module not found | Activate the correct virtual environment and install dependencies. |
| Container exits unexpectedly | Inspect logs using `docker compose logs`. |
| API documentation is unavailable | Verify that the application is running and the correct port is mapped. |

## 🔒 Security Best Practices

- Store credentials in environment variables or a secret manager.
- Keep `.env` files and sensitive configuration out of version control.
- Validate incoming request data.
- Use appropriate database permissions.
- Avoid exposing database ports unnecessarily.
- Use HTTPS and appropriate authentication and authorization for production deployments.

## 🎯 Learning Objectives

This project demonstrates practical concepts in:

- REST API development with FastAPI
- API versioning and route organization
- Relational database integration
- SQLAlchemy ORM
- Containerization with Docker
- Multi-service development using Docker Compose
- API testing and interactive documentation

## 🔮 Future Improvements

Potential enhancements include:

- 🔐 JWT-based authentication and authorization
- 🧪 Automated unit and integration tests
- 📊 Structured logging and monitoring
- 🚀 CI/CD automation with GitHub Actions
- ☁️ Cloud deployment
- 📝 API request and response examples
- 🛡️ Rate limiting and production security hardening

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit your changes with a descriptive message.
5. Open a pull request.


<p align="center">
  ⭐ If you find this project useful, consider giving the repository a star!
</p>

<p align="center">
  <strong>Built with Python, FastAPI, PostgreSQL, and Docker 🐍 ⚡ 🐘 🐳</strong>
</p>
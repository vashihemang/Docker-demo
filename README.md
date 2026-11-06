# <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="20" height="20" alt="FastAPI">&nbsp;&nbsp;FastAPI Health API with <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="20" height="20" alt="Docker">&nbsp;&nbsp;Docker

A FastAPI-based REST API project with PostgreSQL, SQLAlchemy ORM, versioned APIs (V1, V2, V3), and Docker containerization.

---

## 🚀 Technologies Used

<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" alt="Python">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="40" alt="FastAPI">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" alt="PostgreSQL">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="40" alt="Docker">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="40" alt="Git">
</p>

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker
- Docker Compose
- Uvicorn

---

## 📁 Project Structure

```text
Docker-demo/
│
├── main.py
│
├── fastapi_endpoint/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── v1/
│   │   │       └── users.py
│   │   │
│   │   ├── v2/
│   │   │       └── users.py
│   │   │
│   │   └── v3/
│   │           ├── users.py
│   │           └── tasks.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── session.py
│   │
│   └── models/
│       ├── users.py
│       └── tasks.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── README.md
```

## 📌 API Versions & Endpoints

### V1 – User APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/users` | Get all users |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| POST | `/api/v1/users` | Create user |
| PUT | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |

### V2 – User APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v2/users` | Get all users |
| GET | `/api/v2/users/{user_id}` | Get user by ID |
| POST | `/api/v2/users` | Create user |
| PUT | `/api/v2/users/{user_id}` | Update user |
| PATCH | `/api/v2/users/{user_id}` | Partially update user |
| DELETE | `/api/v2/users/{user_id}` | Delete user |

### V3 – User APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v3/users` | Get all users |
| GET | `/api/v3/users/{user_id}` | Get user by ID |
| POST | `/api/v3/users` | Create user |
| PUT | `/api/v3/users/{user_id}` | Update user |
| PATCH | `/api/v3/users/{user_id}` | Partially update user |
| DELETE | `/api/v3/users/{user_id}` | Delete user |
| GET | `/api/v3/users/{user_id}/tasks` | Get user's tasks |

### V3 – Task APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v3/tasks` | Get all tasks |
| GET | `/api/v3/tasks/{task_id}` | Get task by ID |
| POST | `/api/v3/tasks` | Create task |
| PUT | `/api/v3/tasks/{task_id}` | Update task |
| PATCH | `/api/v3/tasks/{task_id}` | Partially update task |
| DELETE | `/api/v3/tasks/{task_id}` | Delete task |

## 🗄️ Database

**PostgreSQL Tables:**

### Users
- id
- name
- email
- phone
- status
- created_at

### Tasks
- id
- title
- description
- status
- user_id (Foreign Key)
- created_at

**Relationship:** One User can have multiple Tasks (One-to-Many).

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/vashihemang/Docker-demo.git
cd Docker-demo
```

### 2. Create Virtual Environment

```bash
python -m venv myenv
```

### 3. Activate Virtual Environment (Windows)

```cmd
myenv\Scripts\activate
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Configure PostgreSQL

Set the database connection URL:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/docker_demo
```

Replace `password` with your PostgreSQL password.

### 6. Run FastAPI Application

```bash
uvicorn fastapi_endpoint.main:app --reload
```

Application URL:

http://127.0.0.1:8000

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t fastapi-demo .
```

### Run Docker Container

```bash
docker run -p 8000:8000 fastapi-demo
```

### Run with Docker Compose

```bash
docker compose up --build
```

### Stop Docker Containers

```bash
docker compose down
```

## 📖 API Documentation

Once the application is running:

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

## 📋 Task Status

- `pending`
- `in_progress`
- `done`

## 👤 User Status

- `active`
- `inactive`

## 🔄 Git Commands

```bash
git add .
git commit -m "Update README documentation"
git push origin main
```


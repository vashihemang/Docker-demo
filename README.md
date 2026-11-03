# FastAPI Health API with Docker
<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg"
       alt="FastAPI" width="100" height="100"/>
  &nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg"
       alt="Docker" width="100" height="100"/>
</p>
A simple REST API built using Python, FastAPI, and Docker.

## Features

- FastAPI application using Python 3.10
- Single GET health-check endpoint
- Dockerized application
- Docker Compose configuration
- Uvicorn ASGI server

## Project Structure

```text
Docker-demo/
├── docker_demo.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

## API Endpoint

**GET /health**

Response:

```json
{
  "status": "ok"
}
```

## Prerequisites

- Python 3.10+
- Docker Desktop
- Docker Compose

## Run with Docker Compose

1. Clone the repository:

```bash
git clone https://github.com/vashihemang/Docker-demo
```

2. Navigate to the project:

```bash
cd Docker-demo
```

3. Build and start the application:

```bash
docker compose up --build -d
```

4. Check running containers:

```bash
docker compose ps
```

5. Test the API:

```text
http://localhost:8000/health
```

6. Open interactive API documentation:

```text
http://localhost:8000/docs
```

## Stop the Application :

```bash
docker compose down
```

## API Testing using Postman :


<img width="1917" height="1020" alt="image" src="https://github.com/user-attachments/assets/e85305a4-cea2-47fc-a053-53ac436ad289" />


## Technologies Used

- Python 3.10
- FastAPI
- Uvicorn
- Docker
- Docker Compose
